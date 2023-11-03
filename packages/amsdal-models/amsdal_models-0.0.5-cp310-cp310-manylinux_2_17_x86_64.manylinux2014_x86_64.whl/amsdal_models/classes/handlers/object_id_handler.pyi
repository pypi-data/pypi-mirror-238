from _typeshed import Incomplete
from amsdal_models.classes.decorators.private_property import PrivateProperty as PrivateProperty
from amsdal_models.classes.handlers.metadata_handler import MetadataHandler as MetadataHandler
from typing import Any

logger: Incomplete

class ObjectIdHandler(MetadataHandler):
    _object_id: str
    _object_version: str
    _is_new_object: bool
    _is_new_object_version: bool
    def __init__(self, **kwargs: Any) -> None: ...
    def object_id(self) -> str: ...
    def is_new_object(self) -> bool: ...
    def object_version(self) -> str: ...
    def is_new_object_version(self) -> bool: ...
