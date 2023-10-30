from typing import List, Optional, Union

import pydantic

from classiq.interface.backend.quantum_backend_providers import ProviderVendor
from classiq.interface.helpers.versioned_model import VersionedModel

from classiq._internals.enum_utils import StrEnum


class AvailabilityStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class DeviceType(StrEnum):
    SIMULATOR = "simulator"
    HARDWARE = "hardware"


class MissingData(StrEnum):
    UNDEFINED = "undefined"


class ExecutionInform(pydantic.BaseModel):
    backend_name: str = pydantic.Field(
        default=...,
        description="The name of the device",
    )
    backend_service_provider: ProviderVendor = pydantic.Field(
        default=...,
        description="The name of the provider",
    )
    status: Union[AvailabilityStatus, MissingData] = pydantic.Field(
        default=...,
        description="availability status of the hardware",
    )
    type: DeviceType = pydantic.Field(
        default=...,
        description="The type of the device",
    )
    max_qubits: Union[int, MissingData] = pydantic.Field(
        default=...,
        description="number of qubits in the hardware",
    )
    average_queue_time: Optional[int] = pydantic.Field(
        default=None,
        description="how many seconds recently run jobs waited in the queue",
    )
    pending_jobs: Optional[int] = pydantic.Field(
        default=None,
        description="number of waiting jobs",
    )


class ExecutionDevicesInform(VersionedModel):
    informs_params: List[ExecutionInform] = pydantic.Field(
        default=...,
        description="List of execution Information of all devices",
    )


class ExecutionInformRequestParams(pydantic.BaseModel):
    provider: ProviderVendor = pydantic.Field(
        default=..., description="List of vendor providers"
    )
