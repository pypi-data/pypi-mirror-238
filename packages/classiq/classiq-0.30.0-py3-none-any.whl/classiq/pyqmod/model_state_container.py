from typing import ClassVar, Dict

from classiq.interface.model.native_function_definition import NativeFunctionDefinition

from classiq import StructDeclaration


class ModelStateContainer:
    TYPE_DECLS: ClassVar[Dict[str, StructDeclaration]]
    NATIVE_DEFS: ClassVar[Dict[str, NativeFunctionDefinition]]
