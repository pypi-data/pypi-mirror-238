from typing import Dict, Tuple

from typing_extensions import TypeAlias

from classiq.interface.backend.quantum_backend_providers import ProviderVendor
from classiq.interface.executor.quantum_instruction_set import QuantumInstructionSet
from classiq.interface.generator.model.preferences.preferences import QuantumFormat

from classiq._internals.enum_utils import StrEnum

Code: TypeAlias = str
CodeAndSyntax: TypeAlias = Tuple[Code, QuantumInstructionSet]

INSTRUCTION_SET_TO_FORMAT: Dict[QuantumInstructionSet, QuantumFormat] = {
    QuantumInstructionSet.QASM: QuantumFormat.QASM,
    QuantumInstructionSet.QSHARP: QuantumFormat.QSHARP,
    QuantumInstructionSet.IONQ: QuantumFormat.IONQ,
}
VENDOR_TO_INSTRUCTION_SET: Dict[str, QuantumInstructionSet] = {
    ProviderVendor.CLASSIQ: QuantumInstructionSet.QASM,
    ProviderVendor.IONQ: QuantumInstructionSet.IONQ,
    ProviderVendor.AZURE_QUANTUM: QuantumInstructionSet.QSHARP,
    ProviderVendor.IBM_QUANTUM: QuantumInstructionSet.QASM,
    ProviderVendor.AMAZON_BRAKET: QuantumInstructionSet.QASM,
}
DEFAULT_INSTRUCTION_SET = QuantumInstructionSet.QASM
_MAXIMUM_STRING_LENGTH = 250


class QasmVersion(StrEnum):
    V2 = "2.0"
    V3 = "3.0"


class LongStr(str):
    def __repr__(self):
        if len(self) > _MAXIMUM_STRING_LENGTH:
            length = len(self)
            return f'"{self[:4]}...{self[-4:]}" (length={length})'
        return super().__repr__()
