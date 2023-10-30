import ast
import builtins
from _ast import AST
from typing import Any, Optional, Set, Tuple, Type, Union

from typing_extensions import get_args

from classiq.interface.generator.arith.ast_node_rewrite import AstNodeRewrite
from classiq.interface.generator.expressions.sympy_supported_expressions import (
    SYMPY_SUPPORTED_EXPRESSIONS,
)

from classiq.exceptions import ClassiqArithmeticError, ClassiqValueError

DEFAULT_SUPPORTED_FUNC_NAMES: Set[str] = {"CLShift", "CRShift", "min", "max"}

DEFAULT_EXPRESSION_TYPE = "arithmetic"

_REPEATED_VARIABLES_ERROR_MESSAGE: str = (
    "Repeated variables in the beginning of an arithmetic expression are not allowed."
)

SupportedNodesTypes = Union[
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.BitOr,
    ast.BitAnd,
    ast.BitXor,
    ast.Invert,
    ast.Compare,
    ast.Eq,
    ast.Mod,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.USub,
    ast.UAdd,
    ast.Sub,
    ast.Gt,
    ast.GtE,
    ast.Lt,
    ast.LtE,
    ast.NotEq,
    ast.LShift,
    ast.RShift,
    ast.Call,
    ast.Mult,
]

DEFAULT_SUPPORTED_NODE_TYPES = get_args(SupportedNodesTypes)


class ExpressionValidator(ast.NodeVisitor):
    def __init__(
        self,
        supported_nodes: Tuple[Type[AST], ...],
        expression_type: str = DEFAULT_EXPRESSION_TYPE,
        supported_functions: Optional[Set[str]] = None,
        supported_attr_values: Optional[Set[str]] = None,
        mode: str = "eval",
    ) -> None:
        super().__init__()
        self.supported_nodes = supported_nodes
        self._expression_type = expression_type
        self._supported_functions = supported_functions or DEFAULT_SUPPORTED_FUNC_NAMES
        self._supported_attr_values = supported_attr_values or set()
        self._mode = mode
        self._ast_obj: Optional[ast.AST] = None

    def validate(self, expression: str) -> None:
        try:
            ast_expr = ast.parse(expression, filename="", mode=self._mode)
        except SyntaxError as e:
            raise ClassiqValueError(f"Failed to parse expression {expression!r}") from e
        try:
            self._ast_obj = AstNodeRewrite().visit(ast_expr)
            self.visit(self._ast_obj)
        except RecursionError as e:
            raise ClassiqValueError(
                f"Failed to parse expression since it is too long: {expression}"
            ) from e

    @property
    def ast_obj(self) -> ast.AST:
        if not self._ast_obj:
            raise ClassiqArithmeticError("Must call `validate` before getting ast_obj")
        return self._ast_obj

    @staticmethod
    def _check_repeated_variables(variables: Tuple[Any, Any]) -> None:
        if (
            all(isinstance(var, ast.Name) for var in variables)
            and variables[0].id == variables[1].id
        ):
            raise ClassiqValueError(_REPEATED_VARIABLES_ERROR_MESSAGE)

    @staticmethod
    def _check_multiple_comparators(node: ast.Compare) -> None:
        if len(node.comparators) > 1:
            raise ClassiqValueError(
                "Arithmetic expression with more than 1 comparator is not supported"
            )

    def generic_visit(self, node: ast.AST) -> None:
        self._validate_node_type(node)
        return super().generic_visit(node)

    def _validate_node_type(self, node: ast.AST) -> None:
        if isinstance(node, self.supported_nodes):
            return
        raise ClassiqValueError(
            f"Invalid {self._expression_type} expression: "
            f"{type(node).__name__} is not supported"
        )

    def validate_Compare(self, node: ast.Compare) -> None:  # noqa: N802
        self._check_repeated_variables((node.left, node.comparators[0]))
        self._check_multiple_comparators(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        self.validate_Compare(node)
        self.generic_visit(node)

    def validate_BinOp(self, node: ast.BinOp) -> None:  # noqa: N802
        self._check_repeated_variables((node.left, node.right))

    def visit_BinOp(self, node: ast.BinOp) -> None:
        self.validate_BinOp(node)
        self.generic_visit(node)

    def validate_Call(self, node: ast.Call) -> None:  # noqa: N802
        if len(node.args) >= 2:
            self._check_repeated_variables((node.args[0], node.args[1]))
        node_id = AstNodeRewrite().extract_node_id(node)
        if node_id not in self._supported_functions:
            raise ClassiqValueError(f"{node_id} not in supported functions")

        if node_id in ("CLShift", "CRShift") and (
            len(node.args) != 2 or not isinstance(node.args[1], ast.Constant)
        ):
            raise ClassiqValueError("Cyclic Shift expects 2 arguments (exp, int)")

    def visit_Call(self, node: ast.Call) -> None:
        self.validate_Call(node)
        self.generic_visit(node)

    def validate_Constant(self, node: ast.Constant) -> None:  # noqa: N802
        if not isinstance(node.value, (int, float, complex, str)):
            raise ClassiqValueError(
                f"{type(node.value).__name__} literals are not valid in {self._expression_type} expressions"
            )

    def visit_Constant(self, node: ast.Constant) -> None:
        self.validate_Constant(node)
        self.generic_visit(node)

    def validate_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802
        if not (
            isinstance(node.value, ast.Name)
            and node.value.id in self._supported_attr_values
        ):
            raise ClassiqValueError(
                f"Attribute is not supported for value {node.value}"
            )

    def visit_Attribute(self, node: ast.Attribute) -> None:
        self.validate_Attribute(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if self._mode == "exec":
            if hasattr(builtins, node.name):
                raise ClassiqValueError(
                    f"Defining a function named {node.name} is forbidden"
                )
            self._supported_functions.add(node.name)
        self.generic_visit(node)


def validate_expression(
    expression: str,
    *,
    supported_nodes: Tuple[Type[AST], ...] = DEFAULT_SUPPORTED_NODE_TYPES,
    expression_type: str = DEFAULT_EXPRESSION_TYPE,
    supported_functions: Optional[Set[str]] = None,
    supported_attr_values: Optional[Set[str]] = None,
    mode: str = "eval",
) -> ast.AST:
    supported_functions = supported_functions or set(SYMPY_SUPPORTED_EXPRESSIONS).union(
        DEFAULT_SUPPORTED_FUNC_NAMES
    )
    validator = ExpressionValidator(
        supported_nodes,
        expression_type,
        supported_functions,
        supported_attr_values,
        mode,
    )
    validator.validate(expression)
    return validator.ast_obj
