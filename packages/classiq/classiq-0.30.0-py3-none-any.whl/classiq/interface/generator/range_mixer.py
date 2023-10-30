import pydantic

from classiq.interface.generator.arith.argument_utils import RegisterOrConst
from classiq.interface.generator.arith.register_user_input import RegisterArithmeticInfo
from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.generator.parameters import ParameterFloatType

DATA_REG_INPUT_NAME: str = "data_reg_input"
LOWER_BOUND_REG_INPUT_NAME: str = "lower_bound_reg_input"
UPPER_BOUND_REG_INPUT_NAME: str = "upper_bound_reg_input"


DATA_REG_OUTPUT_NAME: str = "data_reg_output"
LOWER_BOUND_REG_OUTPUT_NAME: str = "lower_bound_reg_output"
UPPER_BOUND_REG_OUTPUT_NAME: str = "upper_bound_reg_output"


class RangeMixer(FunctionParams):
    """
    Mixing a fixed point number variable between a given lower and upper bounds.
    I.e. after applying this function the variable will hold a
    superposition of all the valid values.
    """

    data_reg_input: RegisterArithmeticInfo = pydantic.Field(
        description="The input variable to mix."
    )

    lower_bound_reg_input: RegisterOrConst = pydantic.Field(
        description="Fixed number or variable that define the lower bound for"
        " the mixing operation. In case of a fixed number bound, the value"
        " must be positive."
    )

    upper_bound_reg_input: RegisterOrConst = pydantic.Field(
        description="Fixed number or variable that define the upper bound for"
        " the mixing operation. In case of a fixed number bound, the value"
        " must be positive."
    )

    mixer_parameter: ParameterFloatType = pydantic.Field(
        description="The parameter used for rotation gates in the mixer.",
        is_exec_param=True,
    )

    def _create_ios(self) -> None:
        self._inputs = {DATA_REG_INPUT_NAME: self.data_reg_input}
        self._outputs = {DATA_REG_OUTPUT_NAME: self.data_reg_input}

        if isinstance(self.lower_bound_reg_input, RegisterArithmeticInfo):
            self._inputs[LOWER_BOUND_REG_INPUT_NAME] = self.lower_bound_reg_input
            self._outputs[LOWER_BOUND_REG_OUTPUT_NAME] = self.lower_bound_reg_input

        if isinstance(self.upper_bound_reg_input, RegisterArithmeticInfo):
            self._inputs[UPPER_BOUND_REG_INPUT_NAME] = self.upper_bound_reg_input
            self._outputs[UPPER_BOUND_REG_OUTPUT_NAME] = self.upper_bound_reg_input
