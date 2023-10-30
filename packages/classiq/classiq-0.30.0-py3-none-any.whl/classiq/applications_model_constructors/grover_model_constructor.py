from typing import Dict, List, Tuple

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.arithmetic_operation import ArithmeticOperation
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.local_variable_declaration import LocalVariableDeclaration
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import (
    QuantumFunctionCall,
    QuantumLambdaFunction,
)
from classiq.interface.model.quantum_type import (
    QuantumFixedReal,
    QuantumInteger,
    QuantumType,
    QuantumUnsignedFixedReal,
    QuantumUnsignedInteger,
)

from classiq import RegisterUserInput

_OUTPUT_VARIABLE_NAME = "result"

_PREDICATE_FUNCTION_NAME = "expr_predicate"


def split_registers(
    register_names: List[str],
    register_sizes: List[int],
    input_wire_name: str,
) -> List[QuantumFunctionCall]:
    if len(register_names) == 0:
        return []
    wires = (
        [input_wire_name]
        + [f"split{i}" for i in range(len(register_names) - 2)]
        + [register_names[-1]]
    )
    return [
        QuantumFunctionCall(
            function="split",
            params={
                "out1_size": Expression(expr=f"{int(register_sizes[i])}"),
                "out2_size": Expression(expr=f"{int(sum(register_sizes[i + 1:]))}"),
            },
            inputs={"in": HandleBinding(name=wires[i])},
            outputs={
                "out1": HandleBinding(name=register),
                "out2": HandleBinding(name=wires[i + 1]),
            },
        )
        for i, register in enumerate(register_names[:-1])
    ]


def _arithmetic_oracle_io_dict(
    definitions: List[Tuple[str, RegisterUserInput]], handle_name: str
) -> Dict[str, HandleBinding]:
    cursor = 0
    ios: Dict[str, HandleBinding] = dict()
    for reg_name, reg in definitions:
        ios[reg_name] = SlicedHandleBinding(
            name=handle_name,
            start=Expression(expr=f"{cursor}"),
            end=Expression(expr=f"{cursor + reg.size}"),
        )
        cursor += reg.size
    return ios


def _construct_arithmetic_oracle(
    predicate_function: str,
    definitions: List[Tuple[str, RegisterUserInput]],
) -> QuantumFunctionCall:
    predicate_var_binding = _arithmetic_oracle_io_dict(definitions, "vars")
    predicate_var_binding["res"] = HandleBinding(name="result")
    return QuantumFunctionCall(
        function="simple_oracle",
        inouts={
            "target": HandleBinding(name="oq"),
        },
        operands={
            "predicate": QuantumLambdaFunction(
                body=[
                    QuantumFunctionCall(
                        function=predicate_function,
                        inouts=predicate_var_binding,
                    ),
                ],
            ),
        },
    )


def get_quantum_type(is_signed: bool, fraction_places: int) -> QuantumType:
    if fraction_places > 0:
        if is_signed:
            return QuantumFixedReal(
                fraction_places=Expression(expr=f"{fraction_places}")
            )
        return QuantumUnsignedFixedReal(
            fraction_places=Expression(expr=f"{fraction_places}")
        )
    if is_signed:
        return QuantumInteger()
    return QuantumUnsignedInteger()


def grover_main_port_declarations(
    definitions: List[Tuple[str, RegisterUserInput]],
    direction: PortDeclarationDirection,
) -> Dict[str, PortDeclaration]:
    return {
        name: PortDeclaration(
            name=name,
            size=Expression(expr=f"{reg.size}"),
            quantum_type=get_quantum_type(reg.is_signed, reg.fraction_places),
            direction=direction,
        )
        for name, reg in definitions
    }


def construct_grover_model(
    definitions: List[Tuple[str, RegisterUserInput]],
    expression: str,
    num_reps: int = 1,
) -> SerializedModel:
    predicate_port_decls = grover_main_port_declarations(
        definitions, PortDeclarationDirection.Inout
    )
    predicate_port_decls["res"] = PortDeclaration(
        name="res",
        size=Expression(expr="1"),
        direction=PortDeclarationDirection.Inout,
    )
    grover_model = Model(
        functions=[
            NativeFunctionDefinition(
                name=_PREDICATE_FUNCTION_NAME,
                port_declarations=predicate_port_decls,
                body=[
                    ArithmeticOperation(
                        expr_str=expression,
                        result_var=HandleBinding(name="res"),
                        inplace_result=True,
                    ),
                ],
            ),
            NativeFunctionDefinition(
                name="main",
                port_declarations=grover_main_port_declarations(
                    definitions, PortDeclarationDirection.Output
                ),
                local_handles=[
                    LocalVariableDeclaration(name="gsq"),
                    *[
                        LocalVariableDeclaration(name=f"split{i}")
                        for i in range(len(definitions) - 2)
                    ],
                ],
                body=[
                    QuantumFunctionCall(
                        function="grover_search",
                        params={
                            "num_qubits": Expression(
                                expr=f"{sum(reg.size for _, reg in definitions)}"
                            ),
                            "reps": Expression(expr=f"{num_reps}"),
                        },
                        outputs={"gsq": HandleBinding(name="gsq")},
                        operands={
                            "oracle_op": QuantumLambdaFunction(
                                body=[
                                    _construct_arithmetic_oracle(
                                        _PREDICATE_FUNCTION_NAME,
                                        definitions,
                                    )
                                ]
                            )
                        },
                    ),
                    *split_registers(
                        [name for name, _ in definitions],
                        [reg.size for _, reg in definitions],
                        "gsq",
                    ),
                ],
            ),
        ],
        classical_execution_code=f"""
{_OUTPUT_VARIABLE_NAME} = sample()
save({{{_OUTPUT_VARIABLE_NAME!r}: {_OUTPUT_VARIABLE_NAME}}})
""",
    )
    return grover_model.get_model()
