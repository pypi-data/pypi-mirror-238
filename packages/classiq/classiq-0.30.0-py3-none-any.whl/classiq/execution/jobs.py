from dataclasses import dataclass, field
from typing import Optional

from classiq.interface.executor.execution_request import (
    ExecuteGeneratedCircuitResults,
    ResultsCollection,
)
from classiq.interface.server.routes import EXECUTE_GENERATED_CIRCUIT_FULL_PATH

from classiq._internals.api_wrapper import _parse_job_response
from classiq._internals.async_utils import syncify_function
from classiq._internals.jobs import JobID, JobPoller


@dataclass
class ExecutionJob:
    id: str
    _result: Optional[ResultsCollection] = field(default=None, repr=False)

    async def result_async(
        self, timeout_sec: Optional[float] = None
    ) -> ResultsCollection:
        if self._result is None:
            self._result = await self._poll_result(timeout_sec=timeout_sec)
        return self._result

    result = syncify_function(result_async)

    async def _poll_result(
        self, timeout_sec: Optional[float] = None
    ) -> ResultsCollection:
        poller = JobPoller(base_url=EXECUTE_GENERATED_CIRCUIT_FULL_PATH)
        response = await poller.poll(
            job_id=JobID(job_id=self.id), timeout_sec=timeout_sec
        )
        raw_result = _parse_job_response(
            job_result=response,
            output_type=ExecuteGeneratedCircuitResults,
        )
        return raw_result.results
