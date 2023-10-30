from dataclasses import dataclass
from typing import Any, Mapping, Type

from typing_extensions import get_args

from classiq.interface.generator.expressions.expression_types import (
    ExpressionValue,
    QmodStructInstance,
    RuntimeConstant,
)
from classiq.interface.generator.expressions.handle_identifier import HandleIdentifier

from classiq.exceptions import ClassiqValueError


@dataclass(frozen=True)
class EvaluatedExpression:
    value: ExpressionValue

    def is_constant(self) -> bool:
        if self.value is None:
            return False

        return isinstance(self.value, get_args(RuntimeConstant))

    def as_constant_type(self, constant_type: Type) -> Any:
        if not self.is_constant():
            raise ClassiqValueError(f"Invalid access to expression as {constant_type}")

        return constant_type(self.value)

    def to_int_value(self) -> int:
        return self.as_constant_type(int)

    def to_bool_value(self) -> bool:
        return self.as_constant_type(bool)

    def to_float_value(self) -> float:
        return self.as_constant_type(float)

    def to_list(self) -> list:
        return self.as_constant_type(list)

    def to_handle(self) -> HandleIdentifier:
        if not isinstance(self.value, HandleIdentifier):
            raise ClassiqValueError(
                f"Invalid access to expression {self.value} as HandleIdentifier"
            )

        return self.value

    def to_struct_dict(self) -> Mapping[str, Any]:
        if not isinstance(self.value, QmodStructInstance):
            raise ClassiqValueError(
                f"Invalid access to expression {self.value} as SympyStructInstance"
            )

        return self.value.fields

    def as_expression(self) -> str:
        if self.value is None:
            raise ClassiqValueError("Invalid access to unevaluated expression")

        return str(self.value)
