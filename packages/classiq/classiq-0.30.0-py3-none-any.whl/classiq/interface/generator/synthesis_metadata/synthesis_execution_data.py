from typing import Dict, Optional, Set

import pydantic

from classiq.interface.backend.pydantic_backend import PydanticExecutionParameter


class FunctionExecutionData(pydantic.BaseModel):
    power_parameter: Optional[PydanticExecutionParameter] = pydantic.Field(default=None)


class ExecutionData(pydantic.BaseModel):
    function_execution: Dict[str, FunctionExecutionData] = pydantic.Field(
        default_factory=dict
    )

    @property
    def execution_parameters(
        self,
    ) -> Set[PydanticExecutionParameter]:
        return {
            function_execution_data.power_parameter
            for function_execution_data in self.function_execution.values()
            if function_execution_data.power_parameter is not None
        }
