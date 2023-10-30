from typing import Any, Dict, List, Optional, Union

import pydantic

from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.parameters import ParameterFloatType, ParameterMap
from classiq.interface.model.arithmetic_operation import ArithmeticOperation
from classiq.interface.model.local_variable_declaration import LocalVariableDeclaration
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)
from classiq.interface.model.validations.handles_validator import HandleValidator

from classiq.exceptions import ClassiqValueError

ConcreteQuantumStatement = Union[QuantumFunctionCall, ArithmeticOperation]


class NativeFunctionDefinition(QuantumFunctionDeclaration):
    """
    Facilitates the creation of a user-defined composite function

    This class sets extra to forbid so that it can be used in a Union and not "steal"
    objects from other classes.
    """

    parameters: List[ParameterMap] = pydantic.Field(
        default_factory=list,
        description="The parameters (name and mapped parameter or value) of the function",
    )

    body: List[ConcreteQuantumStatement] = pydantic.Field(
        default_factory=list, description="List of function calls to perform."
    )

    local_handles: List[LocalVariableDeclaration] = pydantic.Field(
        default_factory=list, description="List of local handles."
    )

    def validate_body(self) -> None:
        handle_validator = HandleValidator(self.port_declarations, self.local_handles)

        for call in self.body:
            handle_validator.handle_call(call)

        handle_validator.report_errored_handles(ClassiqValueError)

    @property
    def parameters_mapping(self) -> Dict[str, ParameterFloatType]:
        return {
            parameter.original: parameter.new_parameter for parameter in self.parameters
        }

    @pydantic.validator("local_handles")
    def validate_local_handles(
        cls, local_handles: List[LocalVariableDeclaration], values: Dict[str, Any]
    ) -> List[LocalVariableDeclaration]:
        ports: Optional[Dict[IOName, PortDeclaration]] = values.get("port_declarations")
        if ports is None:
            return local_handles

        intersection = {handle.name for handle in local_handles} & ports.keys()
        if intersection:
            raise ClassiqValueError(
                f"The names {intersection} are both local handles and ports"
            )

        return local_handles
