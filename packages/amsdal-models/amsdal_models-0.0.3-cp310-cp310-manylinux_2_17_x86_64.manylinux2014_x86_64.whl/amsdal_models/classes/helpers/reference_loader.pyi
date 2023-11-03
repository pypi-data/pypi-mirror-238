from amsdal_models.classes.manager import ClassManager as ClassManager
from amsdal_models.classes.model import Model as Model
from amsdal_utils.models.data_models.reference import Reference as Reference

class ReferenceLoader:
    def __init__(self, reference: Reference) -> None: ...
    def load_reference(self) -> Model: ...
