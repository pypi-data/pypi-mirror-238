from typing import Any, Mapping, Optional

import pydantic
from pydantic import BaseModel

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.function_params import PortDirection

from classiq._internals.enum_utils import StrEnum
from classiq.exceptions import ClassiqValueError

UNRESOLVED_SIZE = 1000


class PortDeclarationDirection(StrEnum):
    Input = "input"
    Inout = "inout"
    Output = "output"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, PortDeclarationDirection):
            return super().__eq__(other)
        if isinstance(other, PortDirection):
            return self == self.Inout or self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def includes_port_direction(self, direction: PortDirection) -> bool:
        return self in (direction, self.Inout)

    @property
    def is_input(self) -> bool:
        return self.includes_port_direction(PortDirection.Input)

    @property
    def is_output(self) -> bool:
        return self.includes_port_direction(PortDirection.Output)

    @classmethod
    def from_port_direction(
        cls, port_direction: PortDirection
    ) -> "PortDeclarationDirection":
        return cls(port_direction.value)


class SynthesisPortDeclaration(BaseModel):
    name: str
    size: Optional[Expression] = pydantic.Field(default=None)
    direction: PortDeclarationDirection
    is_signed: bool = pydantic.Field(default=False)
    fraction_places: Expression = pydantic.Field(default=Expression(expr="0"))

    def get_register_size(self) -> int:
        if self.size is None or not self.size.is_evaluated():
            return UNRESOLVED_SIZE

        return self.size.to_int_value()

    @pydantic.validator("direction")
    def _direction_validator(
        cls, direction: PortDeclarationDirection, values: Mapping[str, Any]
    ) -> PortDeclarationDirection:
        size = values.get("size")
        if direction is PortDeclarationDirection.Output and size is None:
            raise ClassiqValueError("Output ports must have a size")

        return direction
