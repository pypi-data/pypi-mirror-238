from typing import Any, Dict, Generic, TypeVar, Union

import pydantic
from pydantic import BaseModel
from pydantic.generics import GenericModel

from classiq._internals.enum_utils import StrEnum

JSONObject = Dict[str, Any]
T = TypeVar("T", bound=Union[pydantic.BaseModel, JSONObject])
AUTH_HEADER = "Classiq-BE-Auth"


class JobID(BaseModel):
    job_id: str


class JobStatus(StrEnum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    READY = "READY"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"

    def is_final(self) -> bool:
        return self in (self.COMPLETED, self.FAILED, self.CANCELLED)


class JobDescription(GenericModel, Generic[T]):
    status: JobStatus
    description: T
