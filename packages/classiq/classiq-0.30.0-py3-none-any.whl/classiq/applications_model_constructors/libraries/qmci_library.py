from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import (
    QuantumFunctionCall,
    QuantumLambdaFunction,
)
from classiq.interface.model.quantum_function_declaration import (
    QuantumOperandDeclaration,
)

from classiq import Integer

QMCI_LIBRARY = [
    NativeFunctionDefinition(
        name="qmci",
        param_decls={
            "num_phase_qubits": Integer(),
            "num_unitary_qubits": Integer(),
        },
        port_declarations={
            "phase_port": PortDeclaration(
                name="phase_port",
                size=Expression(expr="num_phase_qubits"),
                direction=PortDeclarationDirection.Output,
            ),
            "unitary_port": PortDeclaration(
                name="unitary_port",
                size=Expression(expr="num_unitary_qubits"),
                direction=PortDeclarationDirection.Output,
            ),
        },
        operand_declarations={
            "sp_op": QuantumOperandDeclaration(
                name="sp_op",
                param_decls={"num_unitary_qubits": Integer()},
                port_declarations={
                    "reg": PortDeclaration(
                        name="reg",
                        direction=PortDeclarationDirection.Inout,
                        size=Expression(expr="num_unitary_qubits-1"),
                    ),
                    "ind": PortDeclaration(
                        name="ind",
                        direction=PortDeclarationDirection.Inout,
                        size=Expression(expr="1"),
                    ),
                },
            ),
        },
        body=[
            QuantumFunctionCall(
                function="amplitude_estimation",
                params={
                    "num_unitary_qubits": Expression(expr="num_unitary_qubits"),
                    "num_phase_qubits": Expression(expr="num_phase_qubits"),
                },
                outputs={
                    "phase_port": HandleBinding(name="phase_port"),
                    "unitary_port": HandleBinding(name="unitary_port"),
                },
                operands={
                    "oracle_op": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="Z",
                                inouts={
                                    "target": SlicedHandleBinding(
                                        name="oq",
                                        start=Expression(expr="num_unitary_qubits-1"),
                                        end=Expression(expr="num_unitary_qubits"),
                                    ),
                                },
                            ),
                        ]
                    ),
                    "sp_op": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="sp_op",
                                params={
                                    "num_unitary_qubits": Expression(
                                        expr="num_unitary_qubits"
                                    )
                                },
                                inouts={
                                    "reg": SlicedHandleBinding(
                                        name="spq",
                                        start=Expression(expr="0"),
                                        end=Expression(expr="num_unitary_qubits-1"),
                                    ),
                                    "ind": SlicedHandleBinding(
                                        name="spq",
                                        start=Expression(expr="num_unitary_qubits-1"),
                                        end=Expression(expr="num_unitary_qubits"),
                                    ),
                                },
                            )
                        ],
                    ),
                },
            ),
        ],
    ),
]
