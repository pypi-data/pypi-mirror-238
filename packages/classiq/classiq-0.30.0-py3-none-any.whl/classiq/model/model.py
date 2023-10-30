"""Model module, implementing facilities for designing models and generating circuits using Classiq platform."""
from __future__ import annotations

import logging
import tempfile
from contextlib import nullcontext
from typing import IO, Any, ContextManager, Dict, List, Mapping, Optional, Union, cast

from classiq.interface.chemistry.operator import PauliOperator
from classiq.interface.executor.execution_preferences import (
    ExecutionPreferences,
    QaeWithQpeEstimationMethod,
)
from classiq.interface.generator.expressions.enums import Optimizer
from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.functions import SynthesisNativeFunctionDefinition
from classiq.interface.generator.model import (
    Constraints,
    Preferences,
    SynthesisModel as APIModel,
)
from classiq.interface.generator.model.model import MAIN_FUNCTION_NAME, SerializedModel
from classiq.interface.generator.quantum_function_call import (
    SynthesisQuantumFunctionCall,
)

from classiq._internals.async_utils import AsyncifyABC
from classiq.exceptions import ClassiqError, ClassiqValueError
from classiq.model import function_handler
from classiq.quantum_functions.function_library import FunctionLibrary
from classiq.quantum_register import QReg, QRegGenericAlias

_logger = logging.getLogger(__name__)

_SupportedIO = Union[IO, str]

# TODO: Add docstrings for auto generated methods.


ILLEGAL_SETTING_MSG = "Illegal value type provided"


def _pauli_str_to_enums(pauli_str: str) -> str:
    return ", ".join(f"Pauli.{pauli_term}" for pauli_term in pauli_str)


def _pauli_operator_to_qmod(hamiltonian: PauliOperator) -> str:
    if not all(isinstance(summand[1], complex) for summand in hamiltonian.pauli_list):
        raise ClassiqValueError(
            "Supporting only Hamiltonian with numeric coefficients."
        )
    return ", ".join(
        f"struct_literal(PauliTerm, pauli=[{_pauli_str_to_enums(pauli)}], coefficient={cast(complex, coeff).real})"
        for pauli, coeff in hamiltonian.pauli_list
    )


def _file_handler(fp: Optional[_SupportedIO], mode: str = "r") -> ContextManager[IO]:
    if fp is None:
        temp_file = tempfile.NamedTemporaryFile(mode, suffix=".qmod", delete=False)
        print(f"Using temporary file: {temp_file.name!r}")
        return temp_file

    if isinstance(fp, str):
        return open(fp, mode)

    return nullcontext(fp)


DEFAULT_RESULT_NAME = "result"
DEFAULT_AMPLITUDE_ESTIMATION_RESULT_NAME = "estimation"


class Model(function_handler.FunctionHandler, metaclass=AsyncifyABC):
    """Facility to generate circuits, based on the model."""

    def __init__(self, **kwargs: Any) -> None:
        """Init self."""
        super().__init__()
        self._model = APIModel(**kwargs)

    @classmethod
    def from_model(cls, model: APIModel) -> Model:
        return cls(**dict(model))

    @property
    def _body(
        self,
    ) -> List[SynthesisQuantumFunctionCall]:
        return self._model.body

    @property
    def constraints(self) -> Constraints:
        """Get the constraints aggregated in self.

        Returns:
            The constraints data.
        """
        return self._model.constraints

    @constraints.setter
    def constraints(self, value: Any) -> None:
        if not isinstance(value, Constraints):
            raise ClassiqError(ILLEGAL_SETTING_MSG)
        self._model.constraints = value

    @property
    def preferences(self) -> Preferences:
        """Get the preferences aggregated in self.

        Returns:
            The preferences data.
        """
        return self._model.preferences

    @preferences.setter
    def preferences(self, value: Any) -> None:
        if not isinstance(value, Preferences):
            raise ClassiqError(ILLEGAL_SETTING_MSG)
        self._model.preferences = value

    @property
    def execution_preferences(self) -> ExecutionPreferences:
        return self._model.execution_preferences

    @execution_preferences.setter
    def execution_preferences(self, value: Any) -> None:
        if not isinstance(value, ExecutionPreferences):
            raise ClassiqError(ILLEGAL_SETTING_MSG)
        self._model.execution_preferences = value

    def create_inputs(
        self, inputs: Mapping[IOName, QRegGenericAlias]
    ) -> Dict[IOName, QReg]:
        qregs = super().create_inputs(inputs=inputs)
        self._model.set_inputs(inputs, self.input_wires)
        return qregs

    def set_outputs(self, outputs: Mapping[IOName, QReg]) -> None:
        super().set_outputs(outputs=outputs)
        self._model.set_outputs(outputs, self.output_wires)

    def include_library(self, library: FunctionLibrary) -> None:
        """Includes a user-defined custom function library.

        Args:
            library (FunctionLibrary): The custom function library.
        """
        super().include_library(library=library)
        # It is important that the .functions list is shared between the library and
        # the model, as it is modified in-place
        self._model.functions = library._data
        library.remove_function_definition(MAIN_FUNCTION_NAME)
        self._model.functions.append(
            SynthesisNativeFunctionDefinition(name=MAIN_FUNCTION_NAME)
        )

    def get_model(self) -> SerializedModel:
        return self._model.get_model()

    def create_library(self) -> None:
        self._function_library = FunctionLibrary(*self._model.functions)
        self._model.functions = self._function_library._data

    def sample(
        self,
        execution_params: Optional[Dict[str, float]] = None,
    ) -> None:
        execution_params = execution_params or dict()

        self._model.classical_execution_code += classical_sample_function(
            execution_params=execution_params
        )

    def vqe(
        self,
        hamiltonian: PauliOperator,
        maximize: bool,
        optimizer: Optimizer,
        max_iteration: int,
        initial_point: Optional[List[int]] = None,
        tolerance: float = 0,
        step_size: float = 0,
        skip_compute_variance: bool = False,
        alpha_cvar: float = 1,
    ) -> None:
        initial_point = initial_point or []
        vqe_classical_code = f"""
{DEFAULT_RESULT_NAME} = vqe(
    hamiltonian=[{_pauli_operator_to_qmod(hamiltonian)}],
    maximize={maximize},
    initial_point={initial_point},
    optimizer=Optimizer.{optimizer.name},
    max_iteration={max_iteration},
    tolerance={tolerance},
    step_size={step_size},
    skip_compute_variance={skip_compute_variance},
    alpha_cvar={alpha_cvar}
)
save({{{DEFAULT_RESULT_NAME!r}: {DEFAULT_RESULT_NAME}}})
"""

        self._model.classical_execution_code += vqe_classical_code

    def iqae(
        self,
        epsilon: float,
        alpha: float,
        execution_params: Optional[Dict[str, float]] = None,
    ) -> None:
        execution_params = execution_params or {}

        iqae_classical_code = f"""
{DEFAULT_RESULT_NAME} = iqae(
    epsilon={epsilon},
    alpha={alpha},
    execution_params={execution_params}
)
save({{{DEFAULT_RESULT_NAME!r}: {DEFAULT_RESULT_NAME}}})
"""

        self._model.classical_execution_code += iqae_classical_code

    def post_process_amplitude_estimation(
        self,
        estimation_register_size: int,
        estimation_method: QaeWithQpeEstimationMethod,
    ) -> None:
        postprocess_classical_code = f"""
{DEFAULT_AMPLITUDE_ESTIMATION_RESULT_NAME} = qae_with_qpe_result_post_processing(
    {estimation_register_size},
    {estimation_method},
    {DEFAULT_RESULT_NAME}
)
save({{{DEFAULT_AMPLITUDE_ESTIMATION_RESULT_NAME!r}: {DEFAULT_AMPLITUDE_ESTIMATION_RESULT_NAME}}})
"""

        self._model.classical_execution_code += postprocess_classical_code


def classical_sample_function(execution_params: Dict[str, float]) -> str:
    return f"""
{DEFAULT_RESULT_NAME} = sample({execution_params})
save({{{DEFAULT_RESULT_NAME!r}: {DEFAULT_RESULT_NAME}}})
"""
