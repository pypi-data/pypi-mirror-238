from typing_extensions import assert_never

from classiq.interface.generator.expressions.enums.classical_enum import ClassicalEnum


class LadderOperator(ClassicalEnum):
    PLUS = 0
    MINUS = 1

    def __str__(self) -> str:
        if self is LadderOperator.PLUS:
            return "+"
        elif self is LadderOperator.MINUS:
            return "-"
        else:
            assert_never(self)
