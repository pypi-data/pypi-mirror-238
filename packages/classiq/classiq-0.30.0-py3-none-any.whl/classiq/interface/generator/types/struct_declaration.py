from typing import Any, ClassVar, Dict, Mapping

import pydantic

from classiq.interface.generator.functions.classical_type import ConcreteClassicalType
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)

from classiq.exceptions import ClassiqValueError


class StructDeclaration(HashablePydanticBaseModel):
    name: str

    variables: Dict[str, ConcreteClassicalType] = pydantic.Field(
        default_factory=dict,
        description="Dictionary of variable names and their classical type",
    )

    BUILTIN_STRUCT_DECLARATIONS: ClassVar[Dict[str, "StructDeclaration"]] = {}

    def validate_fields(self, fields: Mapping[str, Any]) -> None:
        if set(self.variables.keys()) != {field for field in fields.keys()}:
            raise ClassiqValueError(f"Invalid fields for {self.name} instance")
