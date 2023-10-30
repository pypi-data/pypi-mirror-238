from typing import Dict

from classiq.interface.generator.expressions.enums.classical_enum import ClassicalEnum


class FinanceFunctionType(ClassicalEnum):
    VAR = 0
    SHORTFALL = 1
    X_SQUARE = 2
    EUROPEAN_CALL_OPTION = 3

    @staticmethod
    def from_string(func_str: str) -> "FinanceFunctionType":
        return FINANCE_FUNCTION_STRING[func_str]


FINANCE_FUNCTION_STRING: Dict[str, FinanceFunctionType] = {
    "var": FinanceFunctionType.VAR,
    "expected shortfall": FinanceFunctionType.SHORTFALL,
    "x**2": FinanceFunctionType.X_SQUARE,
    "european call option": FinanceFunctionType.EUROPEAN_CALL_OPTION,
}
