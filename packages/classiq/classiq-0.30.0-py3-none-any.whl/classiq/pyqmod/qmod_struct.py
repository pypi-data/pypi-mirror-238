import dataclasses
from typing import Any, List, Type

from typing_extensions import dataclass_transform

from classiq.interface.generator.functions.classical_type import QStructBase


def _qmod_val_to_expr_str(val: Any) -> str:
    if dataclasses.is_dataclass(type(val)):
        kwargs_str = ", ".join(
            [
                f"{field.name}={_qmod_val_to_expr_str(vars(val)[field.name])}"
                for field in dataclasses.fields(val)
            ]
        )
        return f"struct_literal({type(val).__name__}, {kwargs_str})"

    if isinstance(val, List):
        elements_str = ", ".join([_qmod_val_to_expr_str(elem) for elem in val])
        return f"[{elements_str}]"

    return str(val)


@dataclass_transform()
def QStruct(user_class: Type) -> Type:  # noqa: N802 - for consistency with 'QFunc'
    def _new_repr(self: Any) -> str:
        return _qmod_val_to_expr_str(self)

    user_dataclass = type(
        user_class.__name__,
        (QStructBase, dataclasses.dataclass(user_class)),
        dict(),
    )
    user_dataclass.__repr__ = _new_repr  # type:ignore[assignment]
    return user_dataclass
