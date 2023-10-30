from typing import Any, Dict, List, Literal, MutableMapping, Union

import numpy as np
import pydantic
from pydantic import BaseModel

from classiq.interface.backend.backend_preferences import IonqBackendPreferences
from classiq.interface.executor.estimation import OperatorsEstimation
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.executor.iqae_result import IQAEResult
from classiq.interface.executor.quantum_program import (
    QuantumInstructionSet,
    QuantumProgram,
)
from classiq.interface.executor.result import EstimationResult, ExecutionDetails
from classiq.interface.executor.vqe_result import VQESolverResult
from classiq.interface.generator.generated_circuit import (
    ExecutionCircuit,
    GeneratedCircuit,
)
from classiq.interface.helpers.versioned_model import VersionedModel

from classiq._internals.enum_utils import StrEnum


class GeneratedCircuitExecution(GeneratedCircuit):
    execution_type: Literal["generated_circuit"] = "generated_circuit"


class BareGeneratedCircuitExecution(ExecutionCircuit):
    execution_type: Literal["bare_generated_circuit"] = "bare_generated_circuit"


class QuantumProgramExecution(QuantumProgram):
    execution_type: Literal["quantum_program"] = "quantum_program"


class EstimateOperatorsExecution(OperatorsEstimation):
    execution_type: Literal["estimate_operators"] = "estimate_operators"


ExecutionPayloads = Union[
    GeneratedCircuitExecution,
    BareGeneratedCircuitExecution,
    QuantumProgramExecution,
    EstimateOperatorsExecution,
]


class ExecutionRequest(BaseModel):
    execution_payload: ExecutionPayloads
    preferences: ExecutionPreferences = pydantic.Field(
        default_factory=ExecutionPreferences,
        description="preferences for the execution",
    )

    @pydantic.validator("preferences")
    def validate_ionq_backend(
        cls, preferences: ExecutionPreferences, values: Dict[str, Any]
    ) -> ExecutionPreferences:
        """
        This function implement the following check:
        BE \\ payload | IonQ program | Qasm program | Other
        --------------|--------------|--------------|------
        IonQ backend  |       V      |      V       |   X
        Other backend |       X      |      V       |   V
        Since:
        - We can't execute non-programs on the IonQ backends
        - We can't execute IonQ programs on non-IonQ backends
        """
        quantum_program = values.get("execution_payload")
        is_ionq_backend = isinstance(
            preferences.backend_preferences, IonqBackendPreferences
        )
        if isinstance(quantum_program, QuantumProgram):
            if (
                quantum_program.syntax == QuantumInstructionSet.IONQ
                and not is_ionq_backend
            ):
                raise ValueError("Can only execute IonQ code on IonQ backend.")
        else:
            # If we handle anything other than a program.
            if is_ionq_backend:
                raise ValueError(
                    "IonQ backend supports only execution of QuantumPrograms"
                )
        return preferences


class QuantumProgramExecutionRequest(ExecutionRequest):
    execution_payload: QuantumProgramExecution


class SavedResultValueType(StrEnum):
    Integer = "int"
    Float = "float"
    Boolean = "bool"
    VQESolverResult = "VQESolverResult"
    ExecutionDetails = "ExecutionDetails"
    EstimationResult = "EstimationResult"
    IQAEResult = "IQAEResult"
    Unstructured = "Unstructured"

    @classmethod
    def get_result_type(cls, value: Any) -> "SavedResultValueType":
        return TYPES_MAP.get(value.__class__, SavedResultValueType.Unstructured)


TYPES_MAP: MutableMapping[Any, SavedResultValueType] = {
    int: SavedResultValueType.Integer,
    float: SavedResultValueType.Float,
    bool: SavedResultValueType.Boolean,
    VQESolverResult: SavedResultValueType.VQESolverResult,
    ExecutionDetails: SavedResultValueType.ExecutionDetails,
    EstimationResult: SavedResultValueType.EstimationResult,
    IQAEResult: SavedResultValueType.IQAEResult,
}
NUMPY_TYPES_MAP: MutableMapping[Any, SavedResultValueType] = {
    np.float64: SavedResultValueType.Float,
    np.double: SavedResultValueType.Float,
}
TYPES_MAP.update(NUMPY_TYPES_MAP)

REVERSED_TYPES_MAP = {value: key for key, value in TYPES_MAP.items()}


class SavedResult(BaseModel):
    name: str
    value: Any
    value_type: SavedResultValueType = SavedResultValueType.Unstructured

    @pydantic.root_validator
    def update_result_type(cls, values):
        if values.get("value_type") != SavedResultValueType.Unstructured:
            return values
        value = values.get("value")
        values["value_type"] = SavedResultValueType.get_result_type(value)
        return values

    @pydantic.root_validator
    def parse_value(cls, values):
        value_type = values.get("value_type")
        if value_type == SavedResultValueType.Unstructured:
            return values

        value = values.get("value")
        value_type_cls = REVERSED_TYPES_MAP[value_type]
        if issubclass(value_type_cls, BaseModel) and not isinstance(
            value, value_type_cls
        ):
            values["value"] = value_type_cls.parse_obj(value)

        return values


ResultsCollection = List[SavedResult]


class ExecuteGeneratedCircuitResults(VersionedModel):
    results: ResultsCollection
