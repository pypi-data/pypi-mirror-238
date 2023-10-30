from typing import Any, Dict, Protocol, Sequence, TypeVar

import pydantic


def get_discriminator_field(default: str, **kwargs: Any) -> Any:
    return pydantic.Field(default_factory=lambda: default, **kwargs)


def values_with_discriminator(
    values: Dict[str, Any], discriminator: str, discriminator_value: Any
) -> Dict[str, Any]:
    values.setdefault(discriminator, discriminator_value)
    return values


class Nameable(Protocol):
    name: str


NameableType = TypeVar("NameableType", bound=Nameable)


def nameables_to_dict(nameables: Sequence[NameableType]) -> Dict[str, NameableType]:
    return {value.name: value for value in nameables}
