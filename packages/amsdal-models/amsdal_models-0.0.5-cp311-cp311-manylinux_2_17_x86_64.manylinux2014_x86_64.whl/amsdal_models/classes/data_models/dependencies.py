from typing import Any

from pydantic import BaseModel
from pydantic import Field

from amsdal_models.enums import MetaClasses
from amsdal_models.schemas.manager import BuildSchemasManager


class DependencyModelNames(BaseModel):
    type_model_names: list[str] = Field(default_factory=list)
    core_model_names: list[str] = Field(default_factory=list)
    contrib_model_names: list[str] = Field(default_factory=list)
    user_model_names: list[str] = Field(default_factory=list)
    reference_model_names: list[str] = Field(default_factory=list)

    @classmethod
    def build_from_schemas_manager(cls, schemas_manager: BuildSchemasManager) -> 'DependencyModelNames':
        return cls(
            type_model_names=[schema.title for schema in schemas_manager.type_schemas],
            core_model_names=[schema.title for schema in schemas_manager.core_schemas],
            contrib_model_names=[schema.title for schema in schemas_manager.contrib_schemas],
            user_model_names=[schema.title for schema in schemas_manager.user_schemas],
            reference_model_names=[
                *[
                    _schema.title
                    for _schema in schemas_manager.core_schemas
                    if _schema.meta_class == MetaClasses.CLASS_OBJECT.value
                ],
                *[
                    _schema.title
                    for _schema in schemas_manager.contrib_schemas
                    if _schema.meta_class == MetaClasses.CLASS_OBJECT.value
                ],
                *[
                    _schema.title
                    for _schema in schemas_manager.user_schemas
                    if _schema.meta_class == MetaClasses.CLASS_OBJECT.value
                ],
            ],
        )


class DependencyItem(BaseModel):
    module: tuple[str | None, str]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DependencyItem):
            return self.module == other.module
        return False

    def __hash__(self):
        return hash(self.module)
