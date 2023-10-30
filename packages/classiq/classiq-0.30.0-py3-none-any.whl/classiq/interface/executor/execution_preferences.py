from datetime import timedelta
from typing import Any, Dict, List, Optional, TypeVar, Union

import pydantic

from classiq.interface.backend.backend_preferences import (
    AWS_DEFAULT_JOB_TIMEOUT_SECONDS,
    AwsBackendPreferences,
    BackendPreferencesTypes,
    backend_preferences_field,
)
from classiq.interface.backend.pydantic_backend import MAX_EXECUTION_TIMEOUT_SECONDS
from classiq.interface.backend.quantum_backend_providers import ClassiqAerBackendNames
from classiq.interface.executor.error_mitigation import ErrorMitigationMethod
from classiq.interface.executor.optimizer_preferences import (
    OptimizerPreferences,
    OptimizerType,
)
from classiq.interface.generator.model.preferences.preferences import (
    TranspilationOption,
)
from classiq.interface.generator.model.preferences.randomness import create_random_seed
from classiq.interface.generator.noise_properties import NoiseProperties

from classiq._internals.enum_utils import ReprEnum

DIFFERENT_TIMEOUT_MSG = (
    "Timeout is defined differently in the execution preferences and the "
    "AWS Backend Preferences."
)

TIMEOUT_LARGE_FOR_AWS_MSG = (
    "Timeout is larger than the current allowed limit of "
    f"{timedelta(MAX_EXECUTION_TIMEOUT_SECONDS)}"
)


class QaeWithQpeEstimationMethod(int, ReprEnum):
    MAXIMUM_LIKELIHOOD = 0
    BEST_FIT = 1


class AmplitudeAmplification(pydantic.BaseModel):
    iterations: List[int] = pydantic.Field(
        default_factory=list,
        description="Number or list of numbers of iteration to use",
    )
    growth_rate: float = pydantic.Field(
        default=1.25,
        description="Number of iteration used is set to round(growth_rate**iterations)",
    )
    sample_from_iterations: bool = pydantic.Field(
        default=False,
        description="If True, number of iterations used is picked randomly from "
        "[1, iteration] range",
    )
    num_of_highest_probability_states_to_check: pydantic.PositiveInt = pydantic.Field(
        default=1, description="Then number of highest probability states to check"
    )

    @pydantic.validator("iterations")
    def _validate_iterations(cls, iterations: Union[List[int], int]) -> List[int]:
        if isinstance(iterations, int):
            return [iterations]
        return iterations


class ExecutionPreferences(pydantic.BaseModel):
    timeout_sec: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        description="If set, limits the execution runtime. Value is in seconds. "
        "Not supported on all platforms.",
    )
    amplitude_amplification: AmplitudeAmplification = pydantic.Field(
        default_factory=AmplitudeAmplification,
        description="Settings related to amplitude amplification execution, used during the grover execution.",
    )
    optimizer_preferences: Optional[OptimizerPreferences] = pydantic.Field(
        default_factory=None,
        description="Settings related to VQE execution.",
    )
    error_mitigation_method: Optional[ErrorMitigationMethod] = pydantic.Field(
        default=None,
        description="Error mitigation method. Currently supports complete and tensored "
        "measurement calibration.",
    )
    noise_properties: Optional[NoiseProperties] = pydantic.Field(
        default=None, description="Properties of the noise in the circuit"
    )
    random_seed: int = pydantic.Field(
        default=None,
        description="The random seed used for the execution",
    )
    backend_preferences: BackendPreferencesTypes = backend_preferences_field(
        backend_name=ClassiqAerBackendNames.AER_SIMULATOR
    )
    num_shots: Optional[pydantic.PositiveInt] = pydantic.Field(default=None)
    transpile_to_hardware: TranspilationOption = pydantic.Field(
        default=TranspilationOption.DECOMPOSE,
        description="Transpile the circuit to the hardware basis gates before execution",
        title="Transpilation Option",
    )

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    @pydantic.validator("num_shots", always=True)
    def validate_num_shots(
        cls, original_num_shots: Optional[pydantic.PositiveInt], values: Dict[str, Any]
    ) -> Optional[pydantic.PositiveInt]:
        return _choose_original_or_optimizer_attribute(
            original_num_shots, "num_shots", None, values
        )

    @pydantic.validator("backend_preferences", always=True)
    def validate_timeout_for_aws(
        cls, backend_preferences: BackendPreferencesTypes, values: Dict[str, Any]
    ) -> BackendPreferencesTypes:
        timeout = values.get("timeout_sec", None)
        if (
            not isinstance(backend_preferences, AwsBackendPreferences)
            or timeout is None
        ):
            return backend_preferences
        if (
            timeout != backend_preferences.job_timeout
            and backend_preferences.job_timeout != AWS_DEFAULT_JOB_TIMEOUT_SECONDS
        ):
            raise ValueError(DIFFERENT_TIMEOUT_MSG)
        if timeout > MAX_EXECUTION_TIMEOUT_SECONDS:
            raise ValueError(TIMEOUT_LARGE_FOR_AWS_MSG)

        backend_preferences.job_timeout = timeout
        return backend_preferences

    @pydantic.validator("random_seed", always=True)
    def validate_random_seed(
        cls, original_random_seed: Optional[int], values: Dict[str, Any]
    ) -> int:
        return _choose_original_or_optimizer_attribute(
            original_random_seed, "random_seed", create_random_seed(), values
        )


T = TypeVar("T")


def _choose_original_or_optimizer_attribute(
    original_attribute: Optional[T],
    attribure_name: str,
    default_value: T,
    values: Dict[str, Any],
) -> T:
    optimizer_preferences = values.get("optimizer_preferences", None)
    optimizer_attribute = getattr(optimizer_preferences, attribure_name, None)

    if original_attribute is None and optimizer_attribute is None:
        return default_value

    elif optimizer_attribute is None:
        # mypy doesn't understand that original_attribute is not None
        return original_attribute  # type: ignore[return-value]

    elif original_attribute is None:
        return optimizer_attribute

    elif original_attribute != optimizer_attribute:
        raise ValueError(
            f"Different {attribure_name} were given for ExecutionPreferences and OptimizerPreferences."
        )

    else:  # This case is original_num_shots == optimizer_num_shots != None
        return original_attribute


__all__ = [
    "ExecutionPreferences",
    "AmplitudeAmplification",
    "ErrorMitigationMethod",
    "NoiseProperties",
    "OptimizerPreferences",
    "OptimizerType",
    "QaeWithQpeEstimationMethod",
]
