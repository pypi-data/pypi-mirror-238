from typing import List

from classiq.interface.generator.function_params import PortDirection
from classiq.interface.generator.functions import SynthesisNativeFunctionDefinition
from classiq.interface.generator.parameters import ParameterMap
from classiq.interface.generator.quantum_function_call import (
    SynthesisQuantumFunctionCall,
)

from classiq.model import function_handler
from classiq.quantum_functions.function_library import FunctionLibrary


class FunctionGenerator(function_handler.FunctionHandler):
    def __init__(self, function_name: str) -> None:
        super().__init__()
        self._name = function_name
        self._logic_flow_list: List[SynthesisQuantumFunctionCall] = list()

    @property
    def _body(self) -> List[SynthesisQuantumFunctionCall]:
        return self._logic_flow_list

    def to_function_definition(self) -> SynthesisNativeFunctionDefinition:
        return SynthesisNativeFunctionDefinition(
            name=self._name,
            body=self._body,
            port_declarations=self._port_declarations,
            input_ports_wiring=self._external_port_wiring[PortDirection.Input],
            output_ports_wiring=self._external_port_wiring[PortDirection.Output],
            parameters=[
                ParameterMap(original=name, new_parameter=name)
                for name in self._parameters
            ],
        )

    def create_library(self) -> None:
        self.include_library(FunctionLibrary())
