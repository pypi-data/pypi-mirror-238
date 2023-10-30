from abc import abstractmethod
from typing import Any, Dict, List, Literal, Union

import pydantic
from pydantic import Extra, Field
from sympy import IndexedBase, Symbol
from typing_extensions import Annotated

from classiq.interface.generator.expressions.enums.ladder_operator import (
    LadderOperator as LadderOperatorEnum,
)
from classiq.interface.generator.expressions.enums.pauli import Pauli as PauliEnum
from classiq.interface.generator.expressions.expression_types import RuntimeExpression
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator

NamedSymbol = Union[IndexedBase, Symbol]


class ClassicalType(HashablePydanticBaseModel):
    def as_symbolic(self, name: str) -> Union[NamedSymbol, List[NamedSymbol]]:
        return Symbol(name)

    @property
    @abstractmethod
    def default_value(self) -> Any:
        raise NotImplementedError(
            f"{self.__class__.__name__} type has no default value"
        )

    @property
    def python_type(self) -> type:
        raise NotImplementedError(
            f"{self.__class__.__name__!r} has no Python SDK equivalent"
        )

    class Config:
        extra = Extra.forbid


class Integer(ClassicalType):
    kind: Literal["int"]

    def as_symbolic(self, name: str) -> Symbol:
        return Symbol(name, integer=True)

    @property
    def default_value(self) -> int:
        return 0

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "int")

    @property
    def python_type(self) -> type:
        return int


class Real(ClassicalType):
    kind: Literal["real"]

    def as_symbolic(self, name: str) -> Symbol:
        return Symbol(name, real=True)

    @property
    def default_value(self) -> float:
        return 0

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "real")

    @property
    def python_type(self) -> type:
        return float


class Bool(ClassicalType):
    kind: Literal["bool"]

    @property
    def default_value(self) -> bool:
        return False

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "bool")

    @property
    def python_type(self) -> type:
        return bool


class ClassicalList(ClassicalType):
    kind: Literal["list"]
    element_type: "ConcreteClassicalType"

    def as_symbolic(self, name: str) -> Symbol:
        return IndexedBase(name)

    @property
    def default_value(self) -> List:
        return []

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "list")

    @property
    def python_type(self) -> type:
        return List[self.element_type.python_type]  # type:ignore[name-defined]


class Pauli(ClassicalType):
    kind: Literal["pauli"]

    @property
    def default_value(self) -> PauliEnum:
        return PauliEnum.I

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "pauli")

    @property
    def python_type(self) -> type:
        return int


class StructMetaType(ClassicalType):
    kind: Literal["type_proxy"]

    @property
    def default_value(self) -> Any:
        return super().default_value

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "type_proxy")


class QStructBase:  # marker for Qmod structs in the Python SDK
    pass


class Struct(ClassicalType):
    kind: Literal["struct_instance"]
    name: str = pydantic.Field(description="The struct type of the instance")

    @property
    def default_value(self) -> Any:
        return super().default_value

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "struct_instance")

    @property
    def python_type(self) -> type:
        return type(self.name, (QStructBase,), dict())


class ClassicalArray(ClassicalType):
    kind: Literal["array"]
    element_type: "ConcreteClassicalType"
    size: pydantic.PositiveInt

    def as_symbolic(self, name: str) -> list:
        return [self.element_type.as_symbolic(f"{name}_{i}") for i in range(self.size)]

    @property
    def default_value(self) -> Any:
        return super().default_value

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "array")


class OpaqueHandle(ClassicalType):
    @property
    def default_value(self) -> int:
        return 0


class VQEResult(OpaqueHandle):
    kind: Literal["vqe_result"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "vqe_result")


class Histogram(OpaqueHandle):
    kind: Literal["histogram"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "histogram")


class Estimation(OpaqueHandle):
    kind: Literal["estimation_result"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "estimation_result")


class IQAERes(OpaqueHandle):
    kind: Literal["iqae_result"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "iqae_result")


class LadderOperator(ClassicalType):
    kind: Literal["ladder_operator"]

    @property
    def default_value(self) -> LadderOperatorEnum:
        return LadderOperatorEnum.PLUS

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "ladder_operator")

    @property
    def python_type(self) -> type:
        return int


ConcreteClassicalType = Annotated[
    Union[
        Integer,
        Real,
        Bool,
        ClassicalList,
        Pauli,
        StructMetaType,
        Struct,
        ClassicalArray,
        VQEResult,
        Histogram,
        Estimation,
        LadderOperator,
        IQAERes,
    ],
    Field(discriminator="kind"),
]
ClassicalList.update_forward_refs()
ClassicalArray.update_forward_refs()


def as_symbolic(symbols: Dict[str, ClassicalType]) -> Dict[str, RuntimeExpression]:
    return {
        param_name: param_type.as_symbolic(param_name)
        for param_name, param_type in symbols.items()
    }


class QmodPyObject:
    pass
