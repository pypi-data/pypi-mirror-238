from _typeshed import Incomplete
from amsdal_models.classes.base import BaseModel as BaseModel
from amsdal_models.classes.decorators.private_property import PrivateProperty as PrivateProperty
from amsdal_models.classes.utils import build_class_schema_reference as build_class_schema_reference
from amsdal_utils.models.data_models.metadata import Metadata
from typing import Any

logger: Incomplete

class MetadataHandler(BaseModel):
    def __init__(self, **kwargs: Any) -> None: ...
    def build_metadata(self) -> Metadata: ...
    def get_metadata(self) -> Metadata: ...
