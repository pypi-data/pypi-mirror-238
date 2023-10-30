from typing import Callable, Dict, List

from typing_extensions import TypeAlias

from classiq.interface.generator.arith.argument_utils import (
    RegisterOrConst,
    fraction_places,
)
from classiq.interface.generator.arith.binary_ops import BOOLEAN_OP_WITH_FRACTIONS_ERROR

from classiq.exceptions import ClassiqArithmeticError

ArgTypeValidator: TypeAlias = Callable[[List[RegisterOrConst]], None]


def _validate_bitwise_op_args(args: List[RegisterOrConst]) -> None:
    if any(fraction_places(arg) > 0 for arg in args):
        raise ClassiqArithmeticError(BOOLEAN_OP_WITH_FRACTIONS_ERROR)


arg_type_validator_map: Dict[str, ArgTypeValidator] = dict(
    BitXor=_validate_bitwise_op_args,
    BitAnd=_validate_bitwise_op_args,
    BitOr=_validate_bitwise_op_args,
)


def validate_operation_arg_types(operation: str, args: List[RegisterOrConst]) -> None:
    if operation not in arg_type_validator_map:
        return
    arg_type_validator_map[operation](args)
