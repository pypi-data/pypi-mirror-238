import logging
from typing import Any
from typing import ClassVar

from amsdal_data.manager import AmsdalDataManager
from amsdal_data.operations.enums import OperationType
from amsdal_data.transactions.decorators import transaction
from pydantic import ConfigDict
from pydantic import Field
from pydantic._internal._model_construction import ModelMetaclass
from typing_extensions import dataclass_transform

from amsdal_models.classes.base import BaseModel
from amsdal_models.classes.errors import ObjectAlreadyExistsError
from amsdal_models.classes.handlers.reference_handler import ReferenceHandler
from amsdal_models.classes.mixins.model_hooks_mixin import ModelHooksMixin
from amsdal_models.managers.base_manager import BaseManager

logger = logging.getLogger(__name__)


class TypeModel(
    ModelHooksMixin,
    ReferenceHandler,
    BaseModel,
):
    ...


@dataclass_transform(kw_only_default=True, field_specifiers=(Field,))
class AmsdalModelMetaclass(ModelMetaclass):
    def __new__(
        mcs,  # noqa: N804
        cls_name: str,
        bases: tuple[type[Any], ...],
        namespace: dict[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> type:
        cls = super().__new__(mcs, cls_name, bases, namespace, *args, **kwargs)

        if 'objects' in namespace:
            namespace['objects'].model = cls
        else:
            for base in bases:
                if hasattr(base, 'objects'):
                    cls.objects = base.objects.copy(cls=cls)  # type: ignore[attr-defined]
                    break

        return cls  # type: ignore[no-any-return]


class Model(TypeModel, metaclass=AmsdalModelMetaclass):
    objects: ClassVar[BaseManager] = BaseManager()

    def __init__(self, **kwargs: Any) -> None:
        is_new_object = not kwargs.get('_object_id', None)

        self.pre_init(is_new_object=is_new_object, kwargs=kwargs)
        super().__init__(**kwargs)
        self.post_init(is_new_object=is_new_object, kwargs=kwargs)

    @transaction
    def save(self, *, force_insert: bool = False) -> 'Model':
        """
        This method is used to save the Model object into the database.
        By default, the object will be updated in the database if it already exists.
        If force_insert is set to True, the object will be inserted into the database even if it already exists,
        which may result in an ObjectAlreadyExistsError.

        The method first checks if force_insert is True, and if the object already exists in the database.
        If it does, it raises an ObjectAlreadyExistsError.
        Otherwise, it sets the _is_new_object attribute of the Model object to True.

        Then, depending on the value of _is_new_object, the method either creates a new record in the database
        by calling the _create() method or updates the existing record by calling the _update() method.

        Finally, the method returns the saved Model object.

        :param force_insert: A boolean indicating whether to force insert the object into the database,
                             even if it already exists.
        :return: The saved Model object.
        """
        if force_insert:
            if self.objects.filter(_address__object_id=self._object_id).count().execute():
                raise ObjectAlreadyExistsError(address=self._metadata.address)

            self._is_new_object = True

        _is_new_object = self._is_new_object

        if _is_new_object:
            self._create()
        else:
            self._update()

        return self

    @transaction
    def delete(self) -> None:
        self.pre_delete()

        if not self._metadata.is_latest:
            msg = 'Error! Trying to make a new version of an object that is not the latest version!'
            raise ValueError(msg)

        operations_manager = AmsdalDataManager().get_operations_manager()
        operations_manager.perform_operation(obj=self, operation=OperationType.DELETE)
        self.post_delete()

    def _create(self) -> None:
        self.pre_create()
        # TODO: check uniqueness
        operations_manager = AmsdalDataManager().get_operations_manager()
        operations_manager.perform_operation(obj=self, operation=OperationType.CREATE)
        self.post_create()
        self._is_new_object = False

    def _update(self) -> None:
        self.pre_update()

        if not self._metadata.is_latest:
            msg = 'Error! Trying to make a new version of an object that is not the latest version!'
            raise ValueError(msg)

        operations_manager = AmsdalDataManager().get_operations_manager()
        operations_manager.perform_operation(obj=self, operation=OperationType.UPDATE)
        self.post_update()


class LegacyModel(TypeModel, metaclass=AmsdalModelMetaclass):
    model_config = ConfigDict(extra='allow')
