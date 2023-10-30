from typing import (
    TYPE_CHECKING,
    Any,
    ForwardRef,
    Generic,
    Literal,
    Optional,
    Tuple,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from sympy import Basic, Dummy
from sympy.printing.pycode import PythonCodePrinter
from typing_extensions import Annotated, _AnnotatedAlias

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.arithmetic_operation import ArithmeticOperation
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding

from classiq.exceptions import ClassiqValueError
from classiq.pyqmod.qmod_parameter import QParam, QParamScalar
from classiq.pyqmod.quantum_callable import QCallable

ILLEGAL_SLICING_STEP_MSG = "Slicing with a step of a QVar is not supported"
SLICE_OUT_OF_BOUNDS_MSG = "Slice end index out of bounds"


_T = TypeVar("_T")


class FixedPythonCodePrinter(PythonCodePrinter):  # 'xor' is not supported in base class
    _operators = {**PythonCodePrinter._operators, **{"xor": "^"}}


def _python_expr(expr: Basic) -> str:
    return FixedPythonCodePrinter().doprint(
        expr.subs({symbol: symbol.name for symbol in expr.free_symbols})
    )


def get_type_hint_expr(type_hint: Any) -> str:
    if isinstance(type_hint, ForwardRef):  # expression in string literal
        return str(type_hint.__forward_arg__)
    if get_origin(type_hint) == Literal:  # explicit numeric literal
        return str(get_args(type_hint)[0])
    else:
        return str(type_hint)  # implicit numeric literal


class QVar(Generic[_T], Dummy):
    def __new__(cls, name: str, slice_: Optional[Tuple[int, int]] = None) -> "QVar":
        instance = super().__new__(cls, name)
        instance._name = name
        instance._slice = slice_
        return instance

    def get_handle_binding(self) -> HandleBinding:
        if self._slice is not None:
            return SlicedHandleBinding(
                name=self._name,
                start=Expression(expr=str(self._slice[0])),
                end=Expression(expr=str(self._slice[1])),
            )
        return HandleBinding(name=self._name)

    def _insert_arith_operation(self, expr: Basic, inplace: bool) -> None:
        # Fixme: Arithmetic operations are not yet supported on slices (see CAD-12670)
        if TYPE_CHECKING:
            assert QCallable.CURRENT_EXPANDABLE is not None
        QCallable.CURRENT_EXPANDABLE.append_call_to_body(
            ArithmeticOperation(
                expr_str=_python_expr(expr),
                result_var=self.get_handle_binding(),
                inplace_result=inplace,
            )
        )

    def __ior__(self, other: Basic) -> "QVar":
        self._insert_arith_operation(other, False)
        return self

    def __ixor__(self, other: Basic) -> "QVar":
        self._insert_arith_operation(other, True)
        return self

    def __getitem__(self, key: Union[slice, int, QParam]) -> "QVar":
        offset = self._slice[0] if self._slice is not None else 0
        if isinstance(key, slice):
            if key.step is not None:
                raise NotImplementedError(ILLEGAL_SLICING_STEP_MSG)
            new_slice = (offset + key.start, offset + key.stop)
        else:
            new_slice = (offset + key, offset + key + 1)
        if self._slice is not None and new_slice[1] > self._slice[1]:
            raise ClassiqValueError(SLICE_OUT_OF_BOUNDS_MSG)
        return QVar(self._name, new_slice)

    def __len__(self) -> int:
        raise ValueError(
            "len(<var>) is not supported for quantum variables - use <var>.len() instead"
        )

    def len(self) -> "QParamScalar":
        return QParamScalar(name=f"len({self._name})")

    @staticmethod
    def is_qvar_type(type_hint: Any) -> bool:
        if isinstance(type_hint, _AnnotatedAlias):
            return QVar.is_qvar_type(type_hint.__args__[0])
        origin = get_origin(type_hint)
        return type_hint == QVar if origin is None else issubclass(origin, QVar)

    @staticmethod
    def size_expr(type_hint: Any) -> Optional[str]:
        if isinstance(type_hint, _AnnotatedAlias):
            return QVar.size_expr(type_hint.__args__[0])

        if get_origin(type_hint) is None:
            return None

        args = get_args(type_hint)
        if len(args) != 1:
            raise ValueError("QVar accepts exactly one generic parameter")

        return get_type_hint_expr(args[0])

    @staticmethod
    def port_direction(type_hint: Any) -> PortDeclarationDirection:
        if isinstance(type_hint, _AnnotatedAlias):
            assert len(type_hint.__metadata__) >= 1
            assert isinstance(type_hint.__metadata__[0], PortDeclarationDirection)
            return type_hint.__metadata__[0]
        return PortDeclarationDirection.Inout


_Q = TypeVar("_Q", bound=QVar)
Output = Annotated[_Q, PortDeclarationDirection.Output]
Input = Annotated[_Q, PortDeclarationDirection.Input]
