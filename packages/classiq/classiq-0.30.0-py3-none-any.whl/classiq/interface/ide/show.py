import re
from typing import Union

import pydantic

from classiq.interface.analyzer.result import QasmCode
from classiq.interface.generator.generated_circuit import ExecutionCircuit

from classiq import GeneratedCircuit
from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import syncify_function
from classiq.exceptions import ClassiqValueError
from classiq.synthesis import SerializedQuantumProgram

QASM_VERSION_REGEX = re.compile("OPENQASM (\\d*.\\d*);")


async def qasm_show_interactive_async(qasm_code: str) -> None:
    circuit = await ApiWrapper.get_generated_circuit_from_qasm(QasmCode(code=qasm_code))
    circuit.show()  # type: ignore[attr-defined]


qasm_show_interactive = syncify_function(qasm_show_interactive_async)


CANT_PARSE_QUANTUM_PROGRAM_MSG = (
    "Can not parse quantum_program into GeneratedCircuit, \n"
)
CANT_SHOW_EXECUTION_CIRCUIT_MSG = (
    "It looks like the flag `support_circuit_visualization` in the model preferences "
    "has been turned off. \n"
    "The resulting circuit does not support visualization. \n"
    "Make sure to set the flag to True, the default setting, and try again."
)
_Circuit = Union[GeneratedCircuit, ExecutionCircuit]


def show(quantum_program: SerializedQuantumProgram) -> None:
    try:
        circuit = GeneratedCircuit.parse_raw(quantum_program)
    except pydantic.error_wrappers.ValidationError as exc:
        try:
            ExecutionCircuit.parse_raw(quantum_program)
            raise ClassiqValueError(CANT_SHOW_EXECUTION_CIRCUIT_MSG) from None
        except pydantic.error_wrappers.ValidationError:
            raise ClassiqValueError(CANT_PARSE_QUANTUM_PROGRAM_MSG) from exc
    circuit.show()  # type: ignore[attr-defined]
