from typing import Any, Dict, List, Literal, NewType, Optional, Set, Union

import pydantic

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.constant import Constant
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.generator.quantum_function_call import SUFFIX_RANDOMIZER
from classiq.interface.generator.types.combinatorial_problem import (
    CombinatorialOptimizationStructDeclaration,
)
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.helpers.pydantic_model_helpers import (
    get_discriminator_field,
    nameables_to_dict,
)
from classiq.interface.helpers.versioned_model import VersionedModel
from classiq.interface.model.name_resolution import resolve_user_function_calls
from classiq.interface.model.native_function_definition import (
    ConcreteQuantumStatement,
    NativeFunctionDefinition,
)
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)

from classiq.exceptions import ClassiqValueError

USER_MODEL_MARKER = "user"

MAIN_FUNCTION_NAME = "main"
CLASSICAL_ENTRY_FUNCTION_NAME = "cmain"

DEFAULT_PORT_SIZE = 1

SerializedModel = NewType("SerializedModel", str)

ConcreteStructDeclaration = Union[
    CombinatorialOptimizationStructDeclaration, StructDeclaration
]

TYPE_NAME_CONFLICT_BUILTIN = (
    "Type '{name}' conflicts with a builtin type with the same name"
)

TYPE_NAME_CONFLICT_USER = (
    "Type '{name}' conflicts with a previously defined type with the same name"
)


def _create_default_functions() -> List[NativeFunctionDefinition]:
    return [NativeFunctionDefinition(name=MAIN_FUNCTION_NAME)]


class VersionedSerializedModel(VersionedModel):
    model: SerializedModel


class Model(VersionedModel):
    """
    All the relevant data for generating quantum circuit in one place.
    """

    kind: Literal["user"] = get_discriminator_field(USER_MODEL_MARKER)

    # Must be validated before logic_flow
    functions: List[NativeFunctionDefinition] = pydantic.Field(
        default_factory=_create_default_functions,
        description="The user-defined custom type library.",
    )

    types: List[ConcreteStructDeclaration] = pydantic.Field(
        default_factory=list,
        description="The user-defined custom function library.",
    )

    classical_execution_code: str = pydantic.Field(
        description="The classical execution code of the model", default=""
    )

    constants: List[Constant] = pydantic.Field(
        default_factory=list,
    )

    constraints: Constraints = pydantic.Field(default_factory=Constraints)

    execution_preferences: ExecutionPreferences = pydantic.Field(
        default_factory=ExecutionPreferences
    )
    preferences: Preferences = pydantic.Field(default_factory=Preferences)

    @property
    def main_func(self) -> NativeFunctionDefinition:
        return self.function_dict[MAIN_FUNCTION_NAME]  # type:ignore[return-value]

    @property
    def body(self) -> List[ConcreteQuantumStatement]:
        return self.main_func.body

    @pydantic.validator("preferences", always=True)
    def _seed_suffix_randomizer(cls, preferences: Preferences) -> Preferences:
        SUFFIX_RANDOMIZER.seed(preferences.random_seed)
        return preferences

    def _get_qualified_direction(
        self, port_name: str, direction: PortDeclarationDirection
    ) -> PortDeclarationDirection:
        if port_name in self.main_func.port_declarations:
            return PortDeclarationDirection.Inout
        return direction

    @property
    def function_dict(self) -> Dict[str, QuantumFunctionDeclaration]:
        return nameables_to_dict(self.functions)

    @pydantic.root_validator()
    def validate_static_correctness(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        functions: Optional[List[QuantumFunctionDeclaration]] = values.get("functions")
        if functions is None:
            return values

        resolve_user_function_calls(
            values,
            nameables_to_dict(functions),
        )
        for func_def in functions:
            if isinstance(func_def, NativeFunctionDefinition):
                func_def.validate_body()
        return values

    @pydantic.validator("types")
    def types_validator(
        cls, types: List[ConcreteStructDeclaration]
    ) -> List[ConcreteStructDeclaration]:
        user_defined_types: Set[str] = set()
        for ctype in types:
            if ctype.name in StructDeclaration.BUILTIN_STRUCT_DECLARATIONS:
                raise ValueError(TYPE_NAME_CONFLICT_BUILTIN.format(name=ctype.name))
            if ctype.name in user_defined_types:
                raise ValueError(TYPE_NAME_CONFLICT_USER.format(name=ctype.name))
            user_defined_types.add(ctype.name)

        return types

    def get_model(self) -> SerializedModel:
        return SerializedModel(
            self.json(exclude_defaults=True, exclude_unset=True, indent=2)
        )

    @pydantic.validator("functions")
    def _validate_entry_point(
        cls, functions: List[NativeFunctionDefinition]
    ) -> List[NativeFunctionDefinition]:
        function_dict = nameables_to_dict(functions)
        if MAIN_FUNCTION_NAME not in function_dict:
            raise ClassiqValueError("The model must contain a `main` function")
        if any(
            pd.direction != PortDeclarationDirection.Output
            for pd in function_dict[MAIN_FUNCTION_NAME].port_declarations.values()
        ):
            raise ClassiqValueError("Function 'main' cannot declare quantum inputs")

        return functions
