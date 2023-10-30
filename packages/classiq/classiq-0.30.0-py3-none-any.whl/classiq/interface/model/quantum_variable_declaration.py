from typing import Optional

import pydantic
from pydantic import BaseModel

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.quantum_type import ConcreteQuantumType, QuantumBitvector


class QuantumVariableDeclaration(BaseModel):
    name: str
    size: Optional[Expression] = pydantic.Field(default=None)
    quantum_type: ConcreteQuantumType = pydantic.Field(default_factory=QuantumBitvector)
