import types
from typing import TYPE_CHECKING, Any, Mapping

if TYPE_CHECKING:
    from classiq.interface.generator.expressions.expression_types import ExpressionValue
    from classiq.interface.generator.types.struct_declaration import StructDeclaration


class QmodStructInstance:
    def __init__(
        self,
        struct_declaration: "StructDeclaration",
        fields: Mapping[str, "ExpressionValue"],
    ) -> None:
        struct_declaration.validate_fields(fields)
        self.struct_declaration = struct_declaration
        self._fields = fields

    @property
    def fields(self) -> Mapping[str, Any]:
        return types.MappingProxyType(self._fields)

    def __repr__(self) -> str:
        return repr(self._fields)
