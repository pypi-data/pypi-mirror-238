from typing import Any, Mapping

import pydantic

from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.quantum_variable_declaration import (
    QuantumVariableDeclaration,
)

from classiq.exceptions import ClassiqValueError

UNRESOLVED_SIZE = 1000


class PortDeclaration(QuantumVariableDeclaration):
    direction: PortDeclarationDirection

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
