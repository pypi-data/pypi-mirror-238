from _typeshed import Incomplete
from amsdal_models.errors import AmsdalValidationError as AmsdalValidationError
from amsdal_models.schemas.data_models.schema import ObjectSchema as ObjectSchema
from amsdal_models.schemas.loaders.base import OptionsLoaderBase as OptionsLoaderBase

logger: Incomplete

class OptionsExtender:
    def __init__(self, options_reader: OptionsLoaderBase) -> None: ...
    def extend(self, config: ObjectSchema) -> None: ...
    def post_extend(self) -> None: ...
