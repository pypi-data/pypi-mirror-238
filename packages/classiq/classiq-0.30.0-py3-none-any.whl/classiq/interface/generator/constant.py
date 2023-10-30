import pydantic

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import ConcreteClassicalType


class Constant(pydantic.BaseModel):
    name: str
    const_type: ConcreteClassicalType
    value: Expression
