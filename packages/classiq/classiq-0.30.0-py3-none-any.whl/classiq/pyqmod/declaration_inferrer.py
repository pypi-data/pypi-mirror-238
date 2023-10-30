import dataclasses
import inspect
import sys
from typing import Any, Callable, Dict, List, Optional, Type, get_args, get_origin

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalArray,
    ClassicalList,
    ConcreteClassicalType,
    Integer,
    QStructBase,
    Real,
    Struct,
)
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    PositionalArg,
    QuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)

from classiq import StructDeclaration
from classiq.pyqmod.model_state_container import ModelStateContainer
from classiq.pyqmod.qmod_parameter import Array, QParam
from classiq.pyqmod.qmod_variable import QVar, get_type_hint_expr
from classiq.pyqmod.quantum_callable import QCallable
from classiq.pyqmod.utilities import unmangle_keyword

OPERAND_ARG_NAME = "arg{i}"


def _version_portable_get_args(py_type: type) -> tuple:
    if sys.version_info[0:2] < (3, 10):
        return get_args(py_type)  # The result of __class_getitem__
    else:
        return get_args(py_type)[0]


def _python_type_to_qmod(py_type: type) -> Optional[ConcreteClassicalType]:
    if py_type == int:
        return Integer()
    elif py_type == float:
        return Real()
    elif py_type == bool:
        return Bool()
    elif get_origin(py_type) == list:
        return ClassicalList(element_type=_python_type_to_qmod(get_args(py_type)[0]))
    elif get_origin(py_type) == Array:
        array_args = _version_portable_get_args(py_type)
        if len(array_args) != 2:
            raise ValueError(
                "Array accepts two generic parameters in the form 'Array[<element-type>, <size>]'"
            )
        return ClassicalArray(
            element_type=_python_type_to_qmod(array_args[0]),
            size=get_type_hint_expr(array_args[1]),
        )
    elif inspect.isclass(py_type) and issubclass(py_type, QStructBase):
        _add_qmod_struct(py_type)
        return Struct(name=py_type.__name__)
    return None


def _add_qmod_struct(py_type: Type[QStructBase]) -> None:
    if (
        py_type.__name__ in StructDeclaration.BUILTIN_STRUCT_DECLARATIONS
        or py_type.__name__ in ModelStateContainer.TYPE_DECLS.keys()
    ):
        return

    ModelStateContainer.TYPE_DECLS[py_type.__name__] = StructDeclaration(
        name=py_type.__name__,
        variables={
            f.name: _python_type_to_qmod(f.type) for f in dataclasses.fields(py_type)
        },
    )


def _extract_param_decl(name: str, py_type: Any) -> ClassicalParameterDeclaration:
    if len(get_args(py_type)) != 1:
        raise ValueError("QParam takes exactly one generic argument")
    py_type = get_args(py_type)[0]
    return ClassicalParameterDeclaration(
        name=name, classical_type=_python_type_to_qmod(py_type)
    )


def _extract_port_decl(name: str, py_type: Any) -> PortDeclaration:
    size_str = QVar.size_expr(py_type)
    return PortDeclaration(
        name=name,
        direction=QVar.port_direction(py_type),
        size=Expression(expr=size_str) if size_str is not None else None,
    )


def _extract_operand_decl(name: str, py_type: Any) -> QuantumOperandDeclaration:
    qc_args = _version_portable_get_args(py_type)
    arg_dict = {
        OPERAND_ARG_NAME.format(i=i): arg_type for i, arg_type in enumerate(qc_args)
    }
    return QuantumOperandDeclaration(
        name=name,
        positional_arg_declarations=_extract_positional_args(arg_dict),
    )


def _extract_positional_args(args: Dict[str, Any]) -> List[PositionalArg]:
    result: List[PositionalArg] = []
    for name, py_type in args.items():
        if name == "return":
            continue
        name = unmangle_keyword(name)
        if get_origin(py_type) is QParam:
            result.append(_extract_param_decl(name, py_type))
        elif QVar.is_qvar_type(py_type):
            result.append(_extract_port_decl(name, py_type))
        else:
            assert get_origin(py_type) is QCallable
            result.append(_extract_operand_decl(name, py_type))
    return result


def infer_func_decl(py_func: Callable) -> QuantumFunctionDeclaration:
    return QuantumFunctionDeclaration(
        name=unmangle_keyword(py_func.__name__),
        positional_arg_declarations=_extract_positional_args(py_func.__annotations__),
    )
