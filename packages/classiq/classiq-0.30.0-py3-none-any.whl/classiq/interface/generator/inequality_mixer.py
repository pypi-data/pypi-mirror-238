import pydantic

from classiq.interface.generator import function_params
from classiq.interface.generator.arith.argument_utils import RegisterOrConst
from classiq.interface.generator.arith.register_user_input import RegisterArithmeticInfo
from classiq.interface.generator.parameters import ParameterFloatType

DATA_REG_INPUT_NAME: str = "data_reg_input"
BOUND_REG_INPUT_NAME: str = "bound_reg_input"

DATA_REG_OUTPUT_NAME: str = "data_reg_output"
BOUND_REG_OUTPUT_NAME: str = "bound_reg_output"


class InequalityMixer(function_params.FunctionParams):
    """
    Mixing a fixed point number variable below a given upper bound or above a given
    lower bound. i.e. after applying this function the variable will hold a
    superposition position of all the valid values.
    """

    data_reg_input: RegisterArithmeticInfo = pydantic.Field(
        description="The input variable to mix."
    )

    bound_reg_input: RegisterOrConst = pydantic.Field(
        description="Fixed number or variable that define the upper or lower bound for"
        " the mixing operation. In case of a fixed number bound, the value"
        " must be positive."
    )

    mixer_parameter: ParameterFloatType = pydantic.Field(
        description="The parameter used for rotation gates in the mixer.",
        is_exec_param=True,
    )

    is_less_inequality: bool = pydantic.Field(
        default=True,
        description="Whether to mix below or above a certain bound."
        "Less inequality mixes between 0 and the given bound."
        "Greater inequality mixes between the bound and the maximal number allowed by"
        " the number of qubits (i.e 2^n - 1).",
    )

    def _create_ios(self) -> None:
        self._inputs = {DATA_REG_INPUT_NAME: self.data_reg_input}
        self._outputs = {DATA_REG_OUTPUT_NAME: self.data_reg_input}

        if isinstance(self.bound_reg_input, RegisterArithmeticInfo):
            self._inputs[BOUND_REG_INPUT_NAME] = self.bound_reg_input
            self._outputs[BOUND_REG_OUTPUT_NAME] = self.bound_reg_input
