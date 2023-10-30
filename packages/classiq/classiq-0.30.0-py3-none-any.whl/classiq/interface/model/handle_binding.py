from pydantic import BaseModel, Extra

from classiq.interface.generator.expressions.expression import Expression


class HandleBinding(BaseModel):
    name: str

    class Config:
        frozen = True
        extra = Extra.forbid


class SlicedHandleBinding(HandleBinding):
    start: Expression
    end: Expression

    class Config:
        frozen = True
        extra = Extra.forbid
