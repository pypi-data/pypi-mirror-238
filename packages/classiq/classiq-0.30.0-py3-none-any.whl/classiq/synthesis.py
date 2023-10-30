from typing import NewType

import pydantic

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.model.common_model_types import ModelInput, SerializedModelInput
from classiq.interface.model.model import SerializedModel

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import syncify_function

SerializedQuantumProgram = NewType("SerializedQuantumProgram", str)


async def synthesize_async(
    serialized_model: SerializedModelInput,
) -> SerializedQuantumProgram:
    model: ModelInput = pydantic.parse_raw_as(ModelInput, serialized_model)  # type: ignore[arg-type]
    quantum_program = await ApiWrapper.call_generation_task(model)
    return SerializedQuantumProgram(quantum_program.json(indent=2))


synthesize = syncify_function(synthesize_async)


def set_preferences(
    serialized_model: SerializedModelInput, preferences: Preferences
) -> SerializedModelInput:
    model: ModelInput = pydantic.parse_raw_as(ModelInput, serialized_model)  # type: ignore[arg-type]
    model.preferences = preferences
    return model.get_model()  # type: ignore[return-value]


def set_constraints(
    serialized_model: SerializedModelInput, constraints: Constraints
) -> SerializedModelInput:
    model: ModelInput = pydantic.parse_raw_as(ModelInput, serialized_model)  # type: ignore[arg-type]
    model.constraints = constraints
    return model.get_model()  # type: ignore[return-value]


def set_execution_preferences(
    serialized_model: SerializedModelInput, execution_preferences: ExecutionPreferences
) -> SerializedModelInput:
    model: ModelInput = pydantic.parse_raw_as(ModelInput, serialized_model)  # type: ignore[arg-type]
    model.execution_preferences = execution_preferences
    return model.get_model()  # type: ignore[return-value]


__all__ = [
    "SerializedModel",
    "SerializedQuantumProgram",
    "synthesize",
    "set_preferences",
    "set_constraints",
    "set_execution_preferences",
]
