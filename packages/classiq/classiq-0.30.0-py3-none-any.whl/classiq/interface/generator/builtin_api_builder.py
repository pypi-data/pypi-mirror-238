from typing import Any, Iterable

from classiq.interface.generator.functions.classical_function_declaration import (
    ClassicalFunctionDeclaration,
)
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)


def populate_builtin_declarations(decls: Iterable[Any]) -> None:
    for decl in decls:
        if isinstance(decl, QuantumFunctionDeclaration):
            QuantumFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS[decl.name] = decl
        if isinstance(decl, ClassicalFunctionDeclaration):
            ClassicalFunctionDeclaration.FOREIGN_FUNCTION_DECLARATIONS[decl.name] = decl
        if isinstance(decl, StructDeclaration):
            StructDeclaration.BUILTIN_STRUCT_DECLARATIONS[decl.name] = decl
