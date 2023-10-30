import ast
from typing import Dict, List, Mapping, Union

import pydantic

from classiq.interface.generator.arith.arithmetic import (
    ARITHMETIC_EXPRESSION_RESULT_NAME,
    compute_arithmetic_result_size,
)
from classiq.interface.generator.function_params import IOName
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.quantum_statement import QuantumOperation


class VarRefCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.var_names: List[str] = []

    def generic_visit(self, node):
        if isinstance(node, ast.Name):
            self.var_names.append(node.id)
        super().generic_visit(node)


class ArithmeticOperation(QuantumOperation):
    expr_str: str = pydantic.Field(
        description="The expression in terms of quantum variables"
    )
    result_var: HandleBinding = pydantic.Field(
        description="The variable storing the expression result"
    )
    inplace_result: bool = pydantic.Field(
        description="Determines whether the result variable is initialized",
    )
    _var_sizes: Dict[str, int] = pydantic.PrivateAttr(
        default_factory=dict,
    )
    _result_size: int = pydantic.PrivateAttr(
        default=None,
    )

    @property
    def var_handles(self) -> List[HandleBinding]:
        vrc = VarRefCollector()
        vrc.visit(ast.parse(self.expr_str))
        return [HandleBinding(name=name) for name in vrc.var_names]

    @property
    def var_sizes(self) -> Dict[str, int]:
        return self._var_sizes

    def initialize_var_sizes(self, var_sizes: Dict[str, int]) -> None:
        self._var_sizes = var_sizes
        self._result_size = compute_arithmetic_result_size(self.expr_str, var_sizes)

    @property
    def wiring_inouts(
        self,
    ) -> Mapping[IOName, Union[SlicedHandleBinding, HandleBinding]]:
        inouts = {handle.name: handle for handle in self.var_handles}
        if self.inplace_result:
            inouts[ARITHMETIC_EXPRESSION_RESULT_NAME] = self.result_var
        return inouts

    @property
    def wiring_outputs(self) -> Mapping[IOName, HandleBinding]:
        outputs = {}
        if not self.inplace_result:
            outputs[ARITHMETIC_EXPRESSION_RESULT_NAME] = self.result_var
        return outputs

    @property
    def result_size(self) -> int:
        return self._result_size
