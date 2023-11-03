import logging
from typing import Any

from amsdal_utils.utils.identifier import get_identifier
from pydantic import PrivateAttr

from amsdal_models.classes.decorators.private_property import PrivateProperty
from amsdal_models.classes.handlers.metadata_handler import MetadataHandler

logger = logging.getLogger(__name__)


class ObjectIdHandler(MetadataHandler):
    _object_id: str = PrivateAttr()
    _object_version: str = PrivateAttr()
    _is_new_object: bool = PrivateAttr(default=True)
    _is_new_object_version: bool = PrivateAttr(default=True)

    def __init__(self, **kwargs: Any):
        object_id = kwargs.pop('_object_id', None)
        object_version = kwargs.pop('_object_version', None)
        super().__init__(**kwargs)

        if object_id is not None:
            self._object_id = object_id
            self._is_new_object = False
        else:
            self._object_id = get_identifier()
            self._is_new_object = True

        self._object_version = object_version

        if not self._object_version:
            self._object_version = get_identifier()
            self._is_new_object_version = True

    @PrivateProperty
    def object_id(self) -> str:
        return self._object_id

    @PrivateProperty
    def is_new_object(self) -> bool:
        return self._is_new_object

    @PrivateProperty
    def object_version(self) -> str:
        return self._object_version

    @PrivateProperty
    def is_new_object_version(self) -> bool:
        return self._is_new_object_version
