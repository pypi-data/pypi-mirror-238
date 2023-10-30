from typing import Dict, Set

import pydantic
from pydantic import BaseModel

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import (
    ArithmeticIODict,
    IOName,
    PortDirection,
)
from classiq.interface.generator.functions.port_declaration import (
    SynthesisPortDeclaration,
)
from classiq.interface.helpers.validation_helpers import validate_nameables_mapping


class SynthesisQuantumFunctionDeclaration(BaseModel):
    """
    Facilitates the creation of a common quantum function interface object.
    """

    name: str = pydantic.Field(description="The name of the function")

    port_declarations: Dict[IOName, SynthesisPortDeclaration] = pydantic.Field(
        description="The input and output ports of the function.",
        default_factory=dict,
    )

    @property
    def input_set(self) -> Set[IOName]:
        return set(self.inputs.keys())

    @property
    def output_set(self) -> Set[IOName]:
        return set(self.outputs.keys())

    @property
    def inputs(self) -> ArithmeticIODict:
        return _ports_to_registers(self.port_declarations, PortDirection.Input)

    @property
    def outputs(self) -> ArithmeticIODict:
        return _ports_to_registers(self.port_declarations, PortDirection.Output)

    @pydantic.validator("port_declarations")
    def _validate_port_declarations_names(
        cls, port_declarations: Dict[IOName, SynthesisPortDeclaration]
    ) -> Dict[IOName, SynthesisPortDeclaration]:
        validate_nameables_mapping(port_declarations, "Port")
        return port_declarations

    class Config:
        extra = pydantic.Extra.forbid


def _ports_to_registers(
    port_declarations: Dict[IOName, SynthesisPortDeclaration], direction: PortDirection
) -> ArithmeticIODict:
    return {
        name: RegisterUserInput(
            name=name,
            size=(port_decl.get_register_size()),
            is_signed=port_decl.is_signed,
            fraction_places=(
                port_decl.fraction_places.to_int_value()
                if port_decl.fraction_places.is_evaluated()
                else 0
            ),
        )
        for name, port_decl in port_declarations.items()
        if port_decl.direction.includes_port_direction(direction)
    }
