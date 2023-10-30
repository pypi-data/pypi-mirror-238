from typing import TypeVar, Union

from pydantic import BaseModel

from classiq.interface.generator.model.model import (
    SerializedModel as SerializedSynthesisModel,
    SynthesisModel,
)
from classiq.interface.model.model import (
    Model as UserModel,
    SerializedModel as SerializedUserModel,
)

ModelInput = Union[UserModel, SynthesisModel]


class ModelRoot(BaseModel):
    __root__: ModelInput


SerializedModelInput = TypeVar(
    "SerializedModelInput", SerializedSynthesisModel, SerializedUserModel
)
