from abc import ABC
from typing import Any, Dict, List, Literal, Mapping, NewType, Optional, Union

import pydantic

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.constant import Constant
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.functions import (
    SynthesisNativeFunctionDefinition,
    SynthesisPortDeclaration,
    SynthesisQuantumFunctionDeclaration,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.generator.quantum_function_call import (
    SUFFIX_RANDOMIZER,
    SynthesisQuantumFunctionCall,
    WireDict,
    WireName,
)
from classiq.interface.generator.types.combinatorial_problem import (
    CombinatorialOptimizationStructDeclaration,
)
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.helpers.pydantic_model_helpers import (
    get_discriminator_field,
    nameables_to_dict,
)
from classiq.interface.helpers.validation_helpers import is_list_unique
from classiq.interface.helpers.versioned_model import VersionedModel

from classiq import ForeignFunctionDefinition as SynthesisForeignFunctionDefinition
from classiq.exceptions import ClassiqValueError
from classiq.quantum_register import QReg, QRegGenericAlias

MAIN_FUNCTION_NAME = "main"
CLASSICAL_ENTRY_FUNCTION_NAME = "cmain"

DEFAULT_PORT_SIZE = 1


SerializedModel = NewType("SerializedModel", str)

ConcreteStructDeclaration = Union[
    CombinatorialOptimizationStructDeclaration, StructDeclaration
]

# We need to define ConcreteFunctionData so pydantic will know
# what class to use when deserializing from object (pydantic attempts to
# parse as each of the classes in the Union, in order).
ConcreteFunctionDefinition = Union[
    SynthesisForeignFunctionDefinition, SynthesisNativeFunctionDefinition
]

TYPE_LIBRARY_DUPLICATED_TYPE_NAMES = (
    "Cannot have multiple struct types with the same name"
)


def _create_default_functions() -> List[ConcreteFunctionDefinition]:
    return [SynthesisNativeFunctionDefinition(name=MAIN_FUNCTION_NAME)]


class ClassiqBaseModel(VersionedModel, ABC):
    """
    All the relevant data for evaluating execution in one place.
    """

    types: List[ConcreteStructDeclaration] = pydantic.Field(
        default_factory=list,
        description="The user-defined custom function library.",
    )

    constants: List[Constant] = pydantic.Field(
        default_factory=list,
    )

    classical_execution_code: str = pydantic.Field(
        description="The classical execution code of the model", default=""
    )

    execution_preferences: ExecutionPreferences = pydantic.Field(
        default_factory=ExecutionPreferences
    )

    @pydantic.validator("types")
    def types_validator(
        cls, types: List[ConcreteStructDeclaration]
    ) -> List[ConcreteStructDeclaration]:
        if not is_list_unique([struct_type.name for struct_type in types]):
            raise ValueError(TYPE_LIBRARY_DUPLICATED_TYPE_NAMES)

        return types


class ExecutionModel(ClassiqBaseModel):
    pass


class SynthesisModel(ClassiqBaseModel):
    """
    All the relevant data for generating quantum circuit in one place.
    """

    kind: Literal["synthesis"] = get_discriminator_field("synthesis")

    # Must be validated before logic_flow
    functions: List[ConcreteFunctionDefinition] = pydantic.Field(
        default_factory=_create_default_functions,
        description="The quantum functions of the model.",
    )

    constraints: Constraints = pydantic.Field(default_factory=Constraints)
    preferences: Preferences = pydantic.Field(default_factory=Preferences)

    def __init__(
        self,
        *,
        body: Optional[List[SynthesisQuantumFunctionCall]] = None,
        inputs: Optional[WireDict] = None,
        outputs: Optional[WireDict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        if body:
            self.main_func.body.extend(body)
        if inputs:
            self.set_inputs(
                {
                    name: QRegGenericAlias(
                        QReg(DEFAULT_PORT_SIZE), (DEFAULT_PORT_SIZE, 0)
                    )
                    for name in inputs.keys()
                },
                inputs,
            )
        if outputs:
            self.set_outputs(
                {name: QReg(DEFAULT_PORT_SIZE) for name in outputs.keys()}, outputs
            )

    @property
    def main_func(self) -> SynthesisNativeFunctionDefinition:
        return self.function_dict[MAIN_FUNCTION_NAME]  # type:ignore[return-value]

    @property
    def body(self) -> List[SynthesisQuantumFunctionCall]:
        return self.main_func.body

    @property
    def inputs(self) -> WireDict:
        return self.main_func.input_ports_wiring

    def set_inputs(
        self,
        inputs: Mapping[IOName, QRegGenericAlias],
        input_wiring: Mapping[IOName, WireName],
    ) -> None:
        self._update_main_declarations(inputs, PortDeclarationDirection.Input)
        self.main_func.input_ports_wiring.update(input_wiring)

    @property
    def outputs(self) -> WireDict:
        return self.main_func.output_ports_wiring

    def set_outputs(
        self, outputs: Mapping[IOName, QReg], output_wiring: Mapping[IOName, WireName]
    ) -> None:
        self._update_main_declarations(outputs, PortDeclarationDirection.Output)
        self.main_func.output_ports_wiring.update(output_wiring)

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

    def _update_main_declarations(
        self,
        value: Union[Mapping[IOName, QReg], Mapping[IOName, QRegGenericAlias]],
        direction: PortDeclarationDirection,
    ) -> None:
        for port_name, register in value.items():
            if isinstance(register, QReg):
                size = len(register)
                is_signed = getattr(register, "is_signed", False) or False
                fraction_places = getattr(register, "fraction_places", 0) or 0
            else:
                size = register.size if register.size is not None else DEFAULT_PORT_SIZE
                is_signed = False
                fraction_places = (
                    register.fraction_places
                    if register.fraction_places is not None
                    else 0
                )

            self.main_func.port_declarations[port_name] = SynthesisPortDeclaration(
                name=port_name,
                size=Expression(expr=f"{size}"),
                direction=self._get_qualified_direction(port_name, direction),
                is_signed=is_signed,
                fraction_places=Expression(expr=f"{fraction_places}"),
            )

    @property
    def function_dict(self) -> Dict[str, SynthesisQuantumFunctionDeclaration]:
        return nameables_to_dict(self.functions)

    @pydantic.validator("functions", each_item=True)
    def validate_static_correctness(
        cls, func_def: ConcreteFunctionDefinition
    ) -> ConcreteFunctionDefinition:
        if isinstance(func_def, SynthesisNativeFunctionDefinition):
            func_def.validate_body()
        return func_def

    @pydantic.validator("functions")
    def validate_main_function_exists(
        cls, func_defs: List[ConcreteFunctionDefinition]
    ) -> List[ConcreteFunctionDefinition]:
        if MAIN_FUNCTION_NAME not in {func.name for func in func_defs}:
            raise ClassiqValueError("The model must contain a `main` function")
        return func_defs

    def get_model(self) -> SerializedModel:
        return SerializedModel(self.json(exclude_defaults=True, indent=2))

    def classical_model(self) -> ExecutionModel:
        return ExecutionModel(
            types=self.types,
            constants=self.constants,
            classical_execution_code=self.classical_execution_code,
            execution_preferences=self.execution_preferences,
        )
