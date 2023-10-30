from abc import ABC
from types import TracebackType
from typing import Any, Callable, ClassVar, Dict, List, Optional, Type, Union

from typing_extensions import Self

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.arithmetic_operation import ArithmeticOperation
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.local_variable_declaration import LocalVariableDeclaration
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import (
    ArgValue,
    QuantumFunctionCall,
    QuantumLambdaFunction,
)
from classiq.interface.model.quantum_function_declaration import (
    PositionalArg,
    QuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)
from classiq.interface.model.quantum_statement import QuantumStatement

from classiq.pyqmod.qmod_parameter import QParam, create_param
from classiq.pyqmod.qmod_variable import QVar
from classiq.pyqmod.quantum_callable import QCallable, QExpandableInterface
from classiq.pyqmod.utilities import mangle_keyword

ArgType = Union[QParam, QVar, QCallable]


class QExpandable(QCallable, QExpandableInterface, ABC):
    STACK: ClassVar[List["QExpandable"]] = list()

    def __init__(self, py_callable: Callable) -> None:
        self._py_callable = py_callable
        self._local_handles: List[LocalVariableDeclaration] = list()
        self._body: List[QuantumStatement] = list()

    @property
    def local_handles(self) -> List[LocalVariableDeclaration]:
        return self._local_handles

    @property
    def body(self) -> List[QuantumStatement]:
        return self._body

    def __enter__(self) -> Self:
        QExpandable.STACK.append(self)
        QCallable.CURRENT_EXPANDABLE = self
        self._local_handles.clear()
        self._body.clear()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        assert QExpandable.STACK.pop() is self
        QCallable.CURRENT_EXPANDABLE = (
            QExpandable.STACK[-1] if QExpandable.STACK else None
        )

    def expand(self) -> None:
        with self:
            self._py_callable(*self._get_positional_args())

    def infer_rename_params(self) -> Dict[str, str]:
        return {
            decl_name: actual_name
            for decl_name, actual_name in list(
                zip(
                    self.func_decl.param_decls.keys(),
                    self._py_callable.__annotations__.keys(),
                )
            )
            if decl_name != actual_name
        }

    def _add_local_handle(self, binding: HandleBinding) -> None:
        if binding.name not in self.func_decl.port_declarations and not any(
            lh.name == binding.name for lh in self._local_handles
        ):
            self._local_handles.append(LocalVariableDeclaration(name=binding.name))

    def _add_call_local_handles(self, qfunc_call: QuantumFunctionCall) -> None:
        for arg in qfunc_call.positional_args:
            if isinstance(arg, HandleBinding):
                self._add_local_handle(arg)

    def _add_arith_result_handle(self, stmt: ArithmeticOperation) -> None:
        self._add_local_handle(stmt.result_var)

    def append_call_to_body(self, stmt: QuantumStatement) -> None:
        if isinstance(stmt, QuantumFunctionCall):
            self._add_call_local_handles(stmt)
        elif isinstance(stmt, ArithmeticOperation):
            self._add_arith_result_handle(stmt)
        self._body.append(stmt)

    def _get_positional_args(self) -> List[ArgType]:
        result: List[Any] = []
        for arg in self.func_decl.get_positional_arg_decls():
            if isinstance(arg, ClassicalParameterDeclaration):
                rename_dict = self.infer_rename_params()
                actual_name = (
                    rename_dict[arg.name] if arg.name in rename_dict else arg.name
                )
                result.append(create_param(actual_name, arg.classical_type))
            elif isinstance(arg, PortDeclaration):
                result.append(QVar(arg.name))
            else:
                assert isinstance(arg, QuantumOperandDeclaration)
                result.append(QTerminalCallable(arg))
        return result

    def create_quantum_function_call(
        self, *args: Any, **kwargs: Any
    ) -> QuantumFunctionCall:
        return _create_quantum_function_call(self.func_decl, *args, **kwargs)


class QLambdaFunction(QExpandable):
    def __init__(self, decl: QuantumFunctionDeclaration, py_callable: Callable) -> None:
        super().__init__(py_callable)
        self._decl = decl

    @property
    def func_decl(self) -> QuantumFunctionDeclaration:
        return self._decl


class QTerminalCallable(QCallable):
    def __init__(self, decl: QuantumFunctionDeclaration) -> None:
        self._decl = decl

    @property
    def func_decl(self) -> QuantumFunctionDeclaration:
        return self._decl

    def create_quantum_function_call(
        self, *args: Any, **kwargs: Any
    ) -> QuantumFunctionCall:
        return _create_quantum_function_call(self.func_decl, *args, **kwargs)


def _prepare_arg(arg_decl: PositionalArg, val: Any) -> ArgValue:
    if isinstance(arg_decl, ClassicalParameterDeclaration):
        return Expression(expr=str(val))
    elif isinstance(arg_decl, PortDeclaration):
        return val.get_handle_binding()
    else:
        if not isinstance(val, QExpandable):
            val = QLambdaFunction(arg_decl, val)
        if val.local_handles:
            raise ValueError("Locals are not supported in lambda functions")
        val.expand()
        return QuantumLambdaFunction(
            rename_params=val.infer_rename_params(), body=val.body
        )


def _prepare_args(
    decl: QuantumFunctionDeclaration, arg_list: List[Any], kwargs: Dict[str, Any]
) -> List[ArgValue]:
    result = []
    for arg_decl in decl.get_positional_arg_decls():
        if arg_list:
            arg = arg_list.pop(0)
        else:
            arg = kwargs.pop(mangle_keyword(arg_decl.name), None)
            if arg is None:
                raise ValueError(
                    f"{decl.name}() missing required argument for {arg_decl.name!r}"
                )
        result.append(_prepare_arg(arg_decl, arg))

    return result


def _create_quantum_function_call(
    decl: QuantumFunctionDeclaration, *args: Any, **kwargs: Any
) -> QuantumFunctionCall:
    arg_decls = decl.get_positional_arg_decls()
    arg_list = list(args)
    prepared_args = _prepare_args(decl, arg_list, kwargs)

    if kwargs:
        bad_kwarg = next(iter(kwargs))
        if not all(arg_decl.name == bad_kwarg for arg_decl in arg_decls):
            raise ValueError(
                f"{decl.name}() got an unexpected keyword argument {bad_kwarg!r}"
            )
        else:
            raise ValueError(
                f"{decl.name}() got multiple values for argument {bad_kwarg!r}"
            )
    if arg_list:
        raise ValueError(
            f"{decl.name}() takes {len(arg_decls)} arguments but {len(args)} were given"
        )

    return QuantumFunctionCall(function=decl.name, positional_args=prepared_args)
