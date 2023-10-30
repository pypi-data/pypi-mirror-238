from typing import List

import pydantic
from pydantic import BaseModel

from classiq.interface.helpers.versioned_model import VersionedModel


class SemanticDiagnostic(BaseModel):
    message: str
    json_path: str


class ModelSemanticChecksResult(VersionedModel):
    diagnostics: List[SemanticDiagnostic] = pydantic.Field(default_factory=list)
