import pydantic

from classiq.interface.generator.functions.classical_type import ConcreteClassicalType


class ClassicalParameterDeclaration(pydantic.BaseModel):
    name: str
    classical_type: ConcreteClassicalType
