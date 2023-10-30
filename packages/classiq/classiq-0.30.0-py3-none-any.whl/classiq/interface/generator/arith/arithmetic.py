from typing import Any, Dict, Optional, Set

import networkx as nx
import pydantic

from classiq.interface.generator.arith import arithmetic_expression_parser
from classiq.interface.generator.arith.arithmetic_expression_abc import (
    ArithmeticExpressionABC,
)
from classiq.interface.generator.arith.arithmetic_param_getters import (
    id2op,
    operation_allows_target,
)
from classiq.interface.generator.arith.arithmetic_result_builder import (
    ArithmeticResultBuilder,
)
from classiq.interface.generator.arith.register_user_input import RegisterArithmeticInfo

ARITHMETIC_EXPRESSION_TARGET_NAME: str = "arithmetic_target"
ARITHMETIC_EXPRESSION_RESULT_NAME: str = "expression_result"


class Arithmetic(ArithmeticExpressionABC):
    target: Optional[RegisterArithmeticInfo] = None
    inputs_to_save: Set[str] = pydantic.Field(default_factory=set)

    @pydantic.validator("inputs_to_save", always=True)
    def _validate_inputs_to_save(
        cls, inputs_to_save: Set[str], values: Dict[str, Any]
    ) -> Set[str]:
        assert all(reg in values.get("definitions", {}) for reg in inputs_to_save)
        return inputs_to_save

    @staticmethod
    def _validate_expression_graph(graph: nx.DiGraph, values: Dict[str, Any]) -> None:
        target = values.get("target")
        if target is None:
            return

        # Check that the expression graph allows setting the target of the expression
        if not all(
            degree or operation_allows_target(id2op(node))
            for node, degree in graph.out_degree
        ):
            raise ValueError("Expression does not support target assignment")

    def _create_ios(self) -> None:
        self._inputs = {
            name: register
            for name, register in self.definitions.items()
            if name in self._get_literal_set()
            and isinstance(register, RegisterArithmeticInfo)
        }
        self._outputs = {
            name: self._inputs[name]
            for name in self.inputs_to_save
            if name in self._inputs
        }
        # TODO: avoid calling the result builder again, as it is called in validation
        result_info = ArithmeticResultBuilder(
            graph=arithmetic_expression_parser.parse_expression(self.expression),
            definitions=self.definitions,
            max_fraction_places=self.max_fraction_places,
        ).result
        self._outputs[ARITHMETIC_EXPRESSION_RESULT_NAME] = result_info
        if self.target:
            self._inputs[ARITHMETIC_EXPRESSION_TARGET_NAME] = self.target


def get_arithmetic_params(
    expr_str: str, var_sizes: Dict[str, int], enable_target: bool = False
) -> Arithmetic:
    return Arithmetic(
        expression=expr_str,
        definitions={
            name: RegisterArithmeticInfo(size=var_sizes[name])
            for name in var_sizes.keys()
        },
        inputs_to_save=set(var_sizes.keys()),
        # FIXME: generalize inout target to multiple qubits
        target=RegisterArithmeticInfo(size=1) if enable_target else None,
    )


def compute_arithmetic_result_size(expr_str: str, var_sizes: Dict[str, int]) -> int:
    arith_param = get_arithmetic_params(expr_str, var_sizes)
    return arith_param.outputs[ARITHMETIC_EXPRESSION_RESULT_NAME].size
