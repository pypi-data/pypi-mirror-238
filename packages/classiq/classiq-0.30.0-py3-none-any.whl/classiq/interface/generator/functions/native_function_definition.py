from typing import Any, Dict, List, Optional

import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import IOName, PortDirection
from classiq.interface.generator.functions.port_declaration import (
    SynthesisPortDeclaration,
)
from classiq.interface.generator.functions.quantum_function_declaration import (
    SynthesisQuantumFunctionDeclaration,
)
from classiq.interface.generator.parameters import ParameterFloatType, ParameterMap
from classiq.interface.generator.quantum_function_call import (
    SynthesisQuantumFunctionCall,
    WireDict,
    WireName,
)
from classiq.interface.generator.validations import flow_graph

LOGIC_FLOW_DUPLICATE_NAME_ERROR_MSG = (
    "Cannot have multiple function calls with the same name"
)


class IOData(pydantic.BaseModel):
    wire: WireName = pydantic.Field(
        description="The name of the wire of the PortDirection data."
    )
    reg: RegisterUserInput = pydantic.Field(
        description="The register information about the PortDirection data."
    )

    class Config:
        frozen = True


class SynthesisNativeFunctionDefinition(SynthesisQuantumFunctionDeclaration):
    """
    Facilitates the creation of a user-defined composite function

    This class sets extra to forbid so that it can be used in a Union and not "steal"
    objects from other classes.
    """

    parameters: List[ParameterMap] = pydantic.Field(
        default_factory=list,
        description="The parameters (name and mapped parameter or value) of the function",
    )

    input_ports_wiring: Dict[IOName, WireName] = pydantic.Field(
        description="The mapping between the functions input ports, to inner wires",
        default_factory=dict,
    )

    output_ports_wiring: Dict[IOName, WireName] = pydantic.Field(
        description="The mapping between the functions output ports, to inner wires",
        default_factory=dict,
    )

    body: List[SynthesisQuantumFunctionCall] = pydantic.Field(
        default_factory=list, description="List of function calls to perform."
    )

    def validate_body(self) -> None:
        function_call_names = {call.name for call in self.body}
        if len(function_call_names) != len(self.body):
            raise ValueError(LOGIC_FLOW_DUPLICATE_NAME_ERROR_MSG)
        flow_graph.validate_legal_wiring(
            self.body,
            flow_input_names=list(self.input_ports_wiring.values()),
            flow_output_names=list(self.output_ports_wiring.values()),
        )
        flow_graph.validate_acyclic_logic_flow(
            self.body,
            flow_input_names=list(self.input_ports_wiring.values()),
            flow_output_names=list(self.output_ports_wiring.values()),
        )

    @property
    def parameters_mapping(self) -> Dict[str, ParameterFloatType]:
        return {
            parameter.original: parameter.new_parameter for parameter in self.parameters
        }

    @classmethod
    def _validate_direction_ports(
        cls,
        port_declarations: Dict[IOName, SynthesisPortDeclaration],
        directions_external_port_wiring: WireDict,
        direction: PortDirection,
    ) -> None:
        for io_name in directions_external_port_wiring:
            if (
                io_name not in port_declarations
                or not port_declarations[io_name].direction == direction
            ):
                raise ValueError(
                    f"The wired {direction} port {io_name!r} is not declared."
                )

    @pydantic.root_validator
    def validate_ports(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        port_declarations: Optional[
            Dict[IOName, SynthesisPortDeclaration]
        ] = values.get("port_declarations")
        if port_declarations is None:
            return values
        cls._validate_direction_ports(
            port_declarations,
            values.get("input_ports_wiring", dict()),
            PortDirection.Input,
        )
        cls._validate_direction_ports(
            port_declarations,
            values.get("output_ports_wiring", dict()),
            PortDirection.Output,
        )
        return values

    @pydantic.validator("input_ports_wiring", always=True)
    def _populate_input_ports_wiring(
        cls, input_ports_wiring: Dict[IOName, WireName], values: Dict[str, Any]
    ) -> Dict[IOName, WireName]:
        return _validate_ports_wiring_for_direction(
            input_ports_wiring, values, PortDirection.Input
        )

    @pydantic.validator("output_ports_wiring", always=True)
    def _populate_output_ports_wiring(
        cls, output_ports_wiring: Dict[IOName, WireName], values: Dict[str, Any]
    ) -> Dict[IOName, WireName]:
        return _validate_ports_wiring_for_direction(
            output_ports_wiring, values, PortDirection.Output
        )


def _get_single_port_wiring(
    ports_wiring: Dict[IOName, WireName], name: str, direction: PortDirection
) -> WireName:
    direction_id = "out" if direction == PortDirection.Output else "in"
    return ports_wiring.get(name) or f"{name}_{direction_id}"


def _port_declarations_to_wiring(
    ports_wiring: Dict[IOName, WireName],
    port_decls: Dict[IOName, SynthesisPortDeclaration],
    direction: PortDirection,
) -> Dict[IOName, WireName]:
    return {
        name: _get_single_port_wiring(ports_wiring, name, direction)
        for name, port in port_decls.items()
        if port.direction.includes_port_direction(direction)
    }


def _validate_ports_wiring_for_direction(
    ports_wiring: Dict[IOName, WireName],
    values: Dict[str, Any],
    direction: PortDirection,
) -> Dict[IOName, WireName]:
    port_decls = values.get("port_declarations")
    if port_decls is None:
        return ports_wiring
    return _port_declarations_to_wiring(ports_wiring, port_decls, direction)
