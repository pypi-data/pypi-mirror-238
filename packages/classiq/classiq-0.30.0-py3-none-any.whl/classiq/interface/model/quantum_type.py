from typing import Any, Dict, Literal, Optional, Union

import pydantic
from pydantic import Extra

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator


class QuantumType(HashablePydanticBaseModel):
    class Config:
        extra = Extra.forbid

    is_signed: Optional[bool] = pydantic.Field(default=None, const=True)
    fraction_places: Optional[Expression] = pydantic.Field(default=None, const=True)


class QuantumBitvector(QuantumType):
    kind: Literal["qvec"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qvec")


class QuantumSignedNumeric(QuantumType):
    is_signed: bool = pydantic.Field(default=True, const=True)


class QuantumUnsignedNumeric(QuantumType):
    is_signed: bool = pydantic.Field(default=False, const=True)


class QuantumInteger(QuantumSignedNumeric):
    kind: Literal["qint"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qint")


class QuantumUnsignedInteger(QuantumUnsignedNumeric):
    kind: Literal["quint"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "quint")


class QuantumFixedReal(QuantumSignedNumeric):
    kind: Literal["qfixed"]
    fraction_places: Expression = pydantic.Field()

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qfixed")


class QuantumUnsignedFixedReal(QuantumUnsignedNumeric):
    kind: Literal["qufixed"]
    fraction_places: Expression = pydantic.Field()

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qufixed")


ConcreteQuantumType = Union[
    QuantumBitvector,
    QuantumInteger,
    QuantumUnsignedInteger,
    QuantumFixedReal,
    QuantumUnsignedFixedReal,
]
