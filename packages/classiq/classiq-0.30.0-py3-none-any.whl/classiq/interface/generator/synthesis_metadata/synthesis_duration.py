from typing import Optional

import pydantic


class SynthesisStepDurations(pydantic.BaseModel):
    model_preprocessing: Optional[float] = None
    preprocessing: float
    solving: float
    conversion_to_circuit: float
    postprocessing: float

    def total_time(self) -> float:
        return sum(
            time if time is not None else 0
            for time in (
                self.model_preprocessing,
                self.preprocessing,
                self.solving,
                self.conversion_to_circuit,
                self.postprocessing,
            )
        )
