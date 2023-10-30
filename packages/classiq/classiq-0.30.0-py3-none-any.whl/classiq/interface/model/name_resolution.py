from typing import Any, Mapping

from classiq.interface.generator.visitor import Visitor
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)


class UserFunctionCallResolver(Visitor):
    def __init__(
        self,
        quantum_function_dict: Mapping[str, QuantumFunctionDeclaration],
    ) -> None:
        self._quantum_function_dict = quantum_function_dict

    def visit_QuantumFunctionCall(self, fc: QuantumFunctionCall) -> None:
        fc.resolve_function_decl(self._quantum_function_dict)
        self.visit_BaseModel(fc)

    def visit_NativeFunctionDefinition(
        self, func_def: NativeFunctionDefinition
    ) -> None:
        curr_dict = self._quantum_function_dict
        self._quantum_function_dict = {
            **self._quantum_function_dict,
            **func_def.operand_declarations,
        }
        self.visit_BaseModel(func_def)
        self._quantum_function_dict = curr_dict


def resolve_user_function_calls(
    root: Any,
    quantum_function_dict: Mapping[str, QuantumFunctionDeclaration],
) -> None:
    UserFunctionCallResolver(
        {
            **QuantumFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS,
            **quantum_function_dict,
        },
    ).visit(root)
