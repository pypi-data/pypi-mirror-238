import datetime
from typing import List, Optional, Tuple

import pydantic

from classiq.interface.helpers.versioned_model import VersionedModel

from classiq._internals.enum_utils import StrEnum


class Provider(StrEnum):
    IBM_QUANTUM = "IBM Quantum"
    AZURE_QUANTUM = "Azure Quantum"
    AMAZON_BRAKET = "Amazon Braket"
    IONQ = "IonQ"
    CLASSIQ = "Classiq"

    @property
    def id(self):
        return self.value.replace(" ", "-").lower()


ProviderIDEnum = StrEnum("ProviderIDEnum", {p.id: p.id for p in Provider})  # type: ignore[misc]


class AvailabilityStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"

    @property
    def is_available(self):
        return self == self.AVAILABLE


class DeviceType(StrEnum):
    SIMULATOR = "simulator"
    HARDWARE = "hardware"

    @property
    def is_simulator(self):
        return self != self.HARDWARE


class HardwareStatus(pydantic.BaseModel):
    last_update_time: datetime.datetime = pydantic.Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC)
    )
    availability: AvailabilityStatus
    queue_time: Optional[datetime.timedelta]
    pending_jobs: Optional[int]


class HardwareInformation(VersionedModel):
    provider: Provider
    vendor: str
    name: str
    display_name: str
    device_type: DeviceType
    number_of_qubits: int
    connectivity_map: Optional[List[Tuple[int, int]]]
    basis_gates: List[str]
    status: HardwareStatus
