import enum
from typing import Dict

from sympy import Basic, Integer

from classiq.interface.chemistry.elements import ELEMENTS
from classiq.interface.chemistry.ground_state_problem import (
    FermionMapping as LibraryFermionMapping,
)
from classiq.interface.generator.expressions.enums.classical_enum import ClassicalEnum

Element = ClassicalEnum("Element", ELEMENTS)  # type: ignore[call-overload]


class MolecularBasis(enum.Enum):
    sto3g = 0

    def to_sympy(self) -> Basic:
        return Integer(self.value)

    @staticmethod
    def sympy_locals() -> Dict[str, Basic]:
        return {f"Basis_{basis.name}": basis.to_sympy() for basis in MolecularBasis}


FermionMapping = ClassicalEnum(  # type: ignore[call-overload]
    "FermionMapping", [mapping.name for mapping in LibraryFermionMapping]
)
