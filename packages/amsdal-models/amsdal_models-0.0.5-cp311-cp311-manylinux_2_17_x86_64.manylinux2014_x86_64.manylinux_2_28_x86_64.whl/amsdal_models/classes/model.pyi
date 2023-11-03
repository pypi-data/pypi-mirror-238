from _typeshed import Incomplete
from amsdal_models.classes.base import BaseModel as BaseModel
from amsdal_models.classes.errors import ObjectAlreadyExistsError as ObjectAlreadyExistsError
from amsdal_models.classes.handlers.reference_handler import ReferenceHandler as ReferenceHandler
from amsdal_models.classes.mixins.model_hooks_mixin import ModelHooksMixin as ModelHooksMixin
from amsdal_models.managers.base_manager import BaseManager as BaseManager
from pydantic._internal._model_construction import ModelMetaclass
from typing import Any, ClassVar

logger: Incomplete

class TypeModel(ModelHooksMixin, ReferenceHandler, BaseModel): ...

class AmsdalModelMetaclass(ModelMetaclass):
    def __new__(mcs, cls_name: str, bases: tuple[type[Any], ...], namespace: dict[str, Any], *args: Any, **kwargs: Any) -> type: ...

class Model(TypeModel, metaclass=AmsdalModelMetaclass):
    objects: ClassVar[BaseManager]
    def __init__(self, **kwargs: Any) -> None: ...
    _is_new_object: bool
    def save(self, *, force_insert: bool = ...) -> Model:
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
    def delete(self) -> None: ...
    def _create(self) -> None: ...
    def _update(self) -> None: ...

class LegacyModel(TypeModel, metaclass=AmsdalModelMetaclass):
    model_config: Incomplete
