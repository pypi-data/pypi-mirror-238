from __future__ import annotations

import abc
from typing import Iterable, Optional

import pydantic

from classiq.interface.generator.arith import number_utils
from classiq.interface.generator.arith.arithmetic_operations import (
    ArithmeticOperationParams,
)
from classiq.interface.generator.arith.register_user_input import RegisterArithmeticInfo
from classiq.interface.generator.function_params import get_zero_input_name

UNARY_ARG_NAME: str = "arg"


class UnaryOpParams(ArithmeticOperationParams):
    arg: RegisterArithmeticInfo
    inplace: bool = False

    @classmethod
    @abc.abstractmethod
    def _expected_result_size(cls, arg: RegisterArithmeticInfo) -> pydantic.PositiveInt:
        pass

    def actual_result_size(self) -> int:
        return self.output_size or self._expected_result_size(self.arg)

    def garbage_output_size(self) -> pydantic.NonNegativeInt:
        return int(self.is_inplaced()) * max(
            self.arg.size - self.actual_result_size(), 0
        )

    def should_add_zero_inputs(self) -> bool:
        return not self.is_inplaced() or self.should_add_zero_input_for_extension()

    def should_add_zero_input_for_extension(
        self, output_size: Optional[int] = None
    ) -> bool:
        return (output_size or self.result_register.size) > self.arg.size

    def _create_ios(self) -> None:
        self._inputs = {UNARY_ARG_NAME: self.arg}
        self._outputs = {self.output_name: self.result_register}

        zero_input_name = get_zero_input_name(self.output_name)
        if not self.is_inplaced():
            self._outputs[UNARY_ARG_NAME] = self.arg
            zero_input_register = self.result_register
            self._zero_inputs = {zero_input_name: zero_input_register}
            return
        if self.should_add_zero_input_for_extension():
            output_extension_size = self.result_register.size - self.arg.size
            self._create_zero_input_registers({zero_input_name: output_extension_size})
        if self.garbage_output_size() > 0:
            self._outputs[self.garbage_output_name] = RegisterArithmeticInfo(
                size=self.garbage_output_size()
            )

    def is_inplaced(self) -> bool:
        return self.inplace

    def get_params_inplace_options(self) -> Iterable[UnaryOpParams]:
        params_kwargs = self.copy().__dict__
        params_kwargs["inplace"] = True
        yield self.__class__(**params_kwargs)

    class Config:
        arbitrary_types_allowed = True


class BitwiseInvert(UnaryOpParams):
    output_name = "inverted"

    @classmethod
    def _expected_result_size(cls, arg: RegisterArithmeticInfo) -> pydantic.PositiveInt:
        return arg.size

    def _get_result_register(self) -> RegisterArithmeticInfo:
        return RegisterArithmeticInfo(
            size=self.actual_result_size(),
            fraction_places=self.arg.fraction_places,
            is_signed=self.arg.is_signed and self._include_sign,
        )


class Negation(UnaryOpParams):
    output_name = "negated"

    @classmethod
    def _expected_result_size(cls, arg: RegisterArithmeticInfo) -> pydantic.PositiveInt:
        if arg.size == 1:
            return 1
        return arg.fraction_places + number_utils.bounds_to_integer_part_size(
            *(-bound for bound in arg.bounds)
        )

    def _get_result_register(self) -> RegisterArithmeticInfo:
        is_signed = max(self.arg.bounds) > 0 and self._include_sign
        bounds = (-max(self.arg.bounds), -min(self.arg.bounds))
        return RegisterArithmeticInfo(
            size=self.actual_result_size(),
            fraction_places=self.arg.fraction_places,
            is_signed=is_signed,
            bounds=bounds if (is_signed or min(bounds) >= 0) else None,
        )


class Sign(UnaryOpParams):
    output_name = "sign"

    @pydantic.validator("output_size")
    def _validate_output_size(
        cls, output_size: Optional[pydantic.PositiveInt]
    ) -> pydantic.PositiveInt:
        if output_size is not None and output_size != 1:
            raise ValueError("Sign output size must be 1")
        return 1

    @classmethod
    def _expected_result_size(cls, arg: RegisterArithmeticInfo) -> pydantic.PositiveInt:
        return 1

    def _get_result_register(self) -> RegisterArithmeticInfo:
        return RegisterArithmeticInfo(size=1, fraction_places=0, is_signed=False)

    def is_inplaced(self) -> bool:
        return self.inplace and self.arg.is_signed
