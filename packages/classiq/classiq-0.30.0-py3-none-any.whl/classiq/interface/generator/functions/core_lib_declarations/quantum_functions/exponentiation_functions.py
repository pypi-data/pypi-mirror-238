from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import (
    ClassicalList,
    Integer,
    Pauli,
    Real,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.types.builtin_struct_declarations.pauli_struct_declarations import (
    Hamiltonian,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)

SINGLE_PAULI_EXPONENT_FUNCTION = QuantumFunctionDeclaration(
    name="single_pauli_exponent",
    param_decls={
        "pauli_string": ClassicalList(element_type=Pauli()),
        "coefficient": Real(),
    },
    port_declarations={
        "qbv": PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="len(pauli_string)"),
        )
    },
)


SUZUKI_TROTTER_FUNCTION = QuantumFunctionDeclaration(
    name="suzuki_trotter",
    param_decls={
        "pauli_operator": Hamiltonian(),
        "evolution_coefficient": Real(),
        "order": Integer(),
        "repetitions": Integer(),
    },
    port_declarations={
        "qbv": PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="len(get_field(pauli_operator[0], 'pauli'))"),
        )
    },
)

QDRIFT_FUNCTION = QuantumFunctionDeclaration(
    name="qdrift",
    param_decls={
        "pauli_operator": Hamiltonian(),
        "evolution_coefficient": Real(),
        "num_qdrift": Integer(),
    },
    port_declarations={
        "qbv": PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="len(get_field(pauli_operator[0], 'pauli'))"),
        )
    },
)

__all__ = [
    "SINGLE_PAULI_EXPONENT_FUNCTION",
    "SUZUKI_TROTTER_FUNCTION",
    "QDRIFT_FUNCTION",
]
