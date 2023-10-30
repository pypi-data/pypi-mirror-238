import functools
import itertools
import re
from collections import defaultdict
from typing import (
    TYPE_CHECKING,
    Any,
    Collection,
    Dict,
    Iterable,
    List,
    Mapping,
    Match,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import pydantic
from pydantic import BaseModel

from classiq.interface.generator import function_param_list, function_params as f_params
from classiq.interface.generator.arith.arithmetic import Arithmetic
from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.function_call import (
    FunctionCall,
    OperandIdentifier,
    check_params_against_declaration,
)
from classiq.interface.generator.function_params import (
    NAME_REGEX,
    FunctionParams,
    IOName,
    PortDirection,
)
from classiq.interface.generator.functions import FunctionDeclaration
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.quantum_function_call import (
    BAD_CALL_NAME_ERROR_MSG,
    BAD_INPUT_ERROR_MSG,
    BAD_INPUT_EXPRESSION_MSG,
    BAD_INPUT_SLICING_MSG,
    BAD_OUTPUT_ERROR_MSG,
    BAD_OUTPUT_EXPRESSION_MSG,
    BAD_OUTPUT_SLICING_MSG,
    CUSTOM_FUNCTION_SINGLE_IO_ERROR,
    LEGAL_SLICING,
    SUFFIX_MARKER,
    randomize_suffix,
)
from classiq.interface.generator.slice_parsing_utils import (
    IO_REGEX,
    NAME,
    SLICING,
    parse_io_slicing,
)
from classiq.interface.generator.user_defined_function_params import CustomFunction
from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_statement import QuantumOperation
from classiq.interface.model.validation_handle import get_unique_handle_names

from classiq.exceptions import ClassiqControlError, ClassiqValueError


def _validate_no_duplicated_ports(
    inputs: Mapping[str, HandleBinding],
    outputs: Mapping[str, HandleBinding],
    inouts: Mapping[str, HandleBinding],
) -> None:
    inputs_and_inouts = inputs.keys() & inouts.keys()
    if inputs_and_inouts:
        raise ClassiqValueError(
            f"{inputs_and_inouts} are used as ports in both inputs and inouts"
        )

    outputs_and_inouts = outputs.keys() & inouts.keys()
    if outputs_and_inouts:
        raise ClassiqValueError(
            f"{outputs_and_inouts} are used as ports in both outputs and inouts"
        )


def _validate_no_duplicated_handles(
    inputs: Mapping[str, HandleBinding],
    outputs: Mapping[str, HandleBinding],
    inouts: Mapping[str, HandleBinding],
) -> None:
    inputs_and_inouts = get_unique_handle_names(inputs) & get_unique_handle_names(
        inouts
    )
    if inputs_and_inouts:
        raise ClassiqValueError(
            f"{inputs_and_inouts} are used as handles in both inputs and inouts"
        )

    outputs_and_inouts = get_unique_handle_names(outputs) & get_unique_handle_names(
        inouts
    )
    if outputs_and_inouts:
        raise ClassiqValueError(
            f"{outputs_and_inouts} are used as handles in both outputs and inouts"
        )


def _validate_no_mixing_sliced_and_whole_handles(
    inouts: Mapping[str, HandleBinding],
) -> None:
    inout_handle_names_to_types = {
        handle_name: {type(handle) for handle in handles}
        for handle_name, handles in itertools.groupby(
            inouts.values(), lambda handle: handle.name
        )
    }
    invalid_handles = [
        handle
        for handle, types in inout_handle_names_to_types.items()
        if len(types) > 1
    ]
    if invalid_handles:
        raise ClassiqValueError(
            f"Inout handles {', '.join(invalid_handles)} mix sliced and whole handles"
        )


ArgValue = Union[Expression, "QuantumOperand", SlicedHandleBinding, HandleBinding]


class QuantumFunctionCall(FunctionCall, QuantumOperation):
    function_params: f_params.FunctionParams = pydantic.Field(
        description="The parameters necessary for defining the function",
        default_factory=CustomFunction,
    )
    strict_zero_ios: bool = pydantic.Field(
        default=True,
        description="Enables automated qubit allocation for pre-determined zero inputs "
        "and allows automated qubit release when performing inversion.\n"
        "Setting this flag to False exposes zero inputs and outputs as regular "
        "functional registers, and shifts the responsibility to the user to manually "
        "manage qubit allocation and release.",
    )
    release_by_inverse: bool = pydantic.Field(
        default=False, description="Release zero inputs in inverse call."
    )
    control_states: List[ControlState] = pydantic.Field(
        default_factory=list,
        description="Call the controlled function with the given controlled states.",
    )
    should_control: bool = pydantic.Field(
        default=True,
        description="False value indicates this call shouldn't be controlled even if the flow is controlled.",
    )
    inputs: Dict[IOName, HandleBinding] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the input name to the wire it connects to",
    )
    inouts: Dict[IOName, Union[SlicedHandleBinding, HandleBinding]] = pydantic.Field(
        default_factory=dict,
        description="A mapping from in/out name to the wires that connect to it",
    )
    outputs: Dict[IOName, HandleBinding] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the output name to the wire it connects to",
    )
    name: PydanticNonEmptyString = pydantic.Field(
        default=None,
        description="The name of the function instance. "
        "If not set, determined automatically.",
    )
    operands: Dict[str, "QuantumOperand"] = pydantic.Field(
        description="Function calls passed to the operator",
        default_factory=dict,
    )
    positional_args: List[ArgValue] = pydantic.Field(default_factory=list)

    _func_decl: Optional[QuantumFunctionDeclaration] = pydantic.PrivateAttr(
        default=None
    )

    @property
    def func_decl(self) -> Optional[QuantumFunctionDeclaration]:
        return self._func_decl

    def set_func_decl(self, fd: Optional[FunctionDeclaration]) -> None:
        if fd is not None and not isinstance(fd, QuantumFunctionDeclaration):
            raise ClassiqValueError(
                "the declaration of a quantum function call cannot be set to a non-quantum function declaration."
            )
        super().set_func_decl(fd)

    @property
    def wiring_inputs(self) -> Mapping[IOName, HandleBinding]:
        return self.inputs

    @property
    def wiring_inouts(
        self,
    ) -> Mapping[IOName, Union[SlicedHandleBinding, HandleBinding]]:
        return self.inouts

    @property
    def wiring_outputs(self) -> Mapping[IOName, HandleBinding]:
        return self.outputs

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, QuantumFunctionCall) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    @pydantic.validator("name", pre=True, always=True)
    def _create_name(cls, name: Optional[str], values: Dict[str, Any]) -> str:
        """
        generates a name to a user defined-functions as follows:
        <function_name>_<SUFFIX_MARKER>_<random_suffix>
        """
        if name is not None:
            match = re.fullmatch(pattern=NAME_REGEX, string=name)
            if match is None:
                raise ValueError(BAD_CALL_NAME_ERROR_MSG)
            return name

        function = values.get("function")
        if isinstance(function, OperandIdentifier):
            function = function.name

        params = values.get("function_params")
        if isinstance(params, CustomFunction):
            if function == CustomFunction.discriminator() and params.name != "":
                function = params.name

        suffix = f"{SUFFIX_MARKER}_{randomize_suffix()}"
        if not function or params is None:
            return name if name else suffix
        return f"{function}_{suffix}"

    @pydantic.root_validator(pre=True)
    def validate_composite_name(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(values.get("unitary_params"), CustomFunction) and not values.get(
            "unitary"
        ):
            raise ClassiqValueError(
                "`PhaseEstimation` of a user define function (`CustomFunction`) must receive the function name from the `unitary` field"
            )
        return values

    @pydantic.root_validator(pre=True)
    def _parse_function_params(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        f_params.parse_function_params_values(
            values=values,
            params_key="function_params",
            discriminator_key="function",
            param_classes=function_param_list.function_param_library.param_list,
            default_parser_class=CustomFunction,
        )
        return values

    @property
    def pos_param_args(self) -> Dict[str, Expression]:
        if TYPE_CHECKING:
            assert self.func_decl is not None
        return dict(
            zip(
                self.func_decl.param_decls.keys(),
                (
                    param
                    for param in self.positional_args
                    if isinstance(param, Expression)
                ),
                strict=True,
            )
        )

    @property
    def pos_operand_args(self) -> Dict[str, "QuantumOperand"]:
        if TYPE_CHECKING:
            assert self.func_decl is not None
        return dict(
            zip(
                self.func_decl.operand_declarations.keys(),
                (
                    param
                    for param in self.positional_args
                    if not isinstance(param, (Expression, HandleBinding))
                ),
                strict=True,
            )
        )

    @property
    def pos_port_args(self) -> Dict[str, HandleBinding]:
        if TYPE_CHECKING:
            assert self.func_decl is not None
        return dict(
            zip(
                self.func_decl.port_declarations.keys(),
                (
                    param
                    for param in self.positional_args
                    if isinstance(param, HandleBinding)
                ),
                strict=True,
            )
        )

    def _update_pos_port_params(self) -> None:
        if TYPE_CHECKING:
            assert self.func_decl is not None
        for name, port_decl in self.func_decl.port_declarations.items():
            if port_decl.direction == PortDeclarationDirection.Input:
                self.inputs[name] = self.pos_port_args[name]
            elif port_decl.direction == PortDeclarationDirection.Output:
                self.outputs[name] = self.pos_port_args[name]
            else:
                self.inouts[name] = self.pos_port_args[name]

    def _reduce_positional_args_to_keywords(self) -> None:
        self.params.update(self.pos_param_args)
        self.operands.update(self.pos_operand_args)
        self._update_pos_port_params()

    # TODO: note that this checks QuantumFunctionCall input register names
    # are PARTIAL to FunctionParams input register names, not EQUAL.
    # We might want to change that.
    @staticmethod
    def _validate_input_names(
        *,
        params: f_params.FunctionParams,
        input_names: Collection[IOName],
        control_states: List[ControlState],
        strict_zero_ios: bool,
    ) -> None:
        (
            invalid_expressions,
            invalid_slicings,
            invalid_names,
        ) = QuantumFunctionCall._get_invalid_ios(
            expressions=input_names,
            params=params,
            io=PortDirection.Input,
            control_states=control_states,
            strict_zero_ios=strict_zero_ios,
        )
        error_msg = []
        if invalid_expressions:
            error_msg.append(f"{BAD_INPUT_EXPRESSION_MSG}: {invalid_expressions}")
        if invalid_names:
            error_msg.append(f"{BAD_INPUT_ERROR_MSG}: {invalid_names}")
        if invalid_slicings:
            error_msg.append(f"{BAD_INPUT_SLICING_MSG}: {invalid_slicings}")
        if error_msg:
            raise ValueError("\n".join(error_msg))

    def resolve_function_decl(
        self,
        function_dict: Mapping[str, FunctionDeclaration],
    ) -> None:
        if not isinstance(self.function_params, CustomFunction):
            return
        super().resolve_function_decl(function_dict)

        if TYPE_CHECKING:
            assert self.func_decl is not None

        if self.positional_args:
            self._reduce_positional_args_to_keywords()

        check_params_against_declaration(
            set(self.params.keys()),
            set(self.func_decl.param_decls.keys()),
            self.func_decl.name,
        )
        _check_ports_against_declaration(self, self.func_decl)
        check_params_against_declaration(
            set(self.operands.keys()),
            set(self.func_decl.operand_declarations.keys()),
            self.func_name,
        )

    @pydantic.validator("strict_zero_ios")
    def _validate_arithmetic_cannot_strict_zero_ios(
        cls, strict_zero_ios: bool, values: Dict[str, Any]
    ) -> bool:
        assert not (
            values.get("function") == Arithmetic.discriminator() and not strict_zero_ios
        ), "when using the Arithmetic function, assign to the expression result register via the target parameter instead of the strict_zero_ios flag"
        return strict_zero_ios

    @pydantic.validator("control_states")
    def _validate_control_states(
        cls, control_states: List[ControlState], values: Dict[str, Any]
    ) -> List[ControlState]:
        control_names = [ctrl_state.name for ctrl_state in control_states]
        function_params = values.get("function_params")
        strict_zero_ios = values.get("strict_zero_ios")
        if not (
            isinstance(function_params, FunctionParams)
            and isinstance(strict_zero_ios, bool)
        ):
            return control_states
        all_input_names = [
            *function_params.inputs_full(strict_zero_ios=strict_zero_ios),
            *control_names,
        ]
        all_output_names = [*function_params.outputs, *control_names]
        if any(
            cls._has_repetitions(name_list)
            for name_list in (control_names, all_input_names, all_output_names)
        ):
            raise ClassiqControlError()
        return control_states

    @staticmethod
    def _has_repetitions(name_list: Sequence[str]) -> bool:
        return len(set(name_list)) < len(name_list)

    @staticmethod
    def _validate_slices(
        io: PortDirection,
        input_names: Collection[IOName],
        fp: FunctionParams,
        strict_zero_ios: bool,
        control_states: List[ControlState],
    ) -> None:
        name_slice_pairs = [parse_io_slicing(input) for input in input_names]
        slices_dict: Dict[str, List[slice]] = defaultdict(list)
        for name, slice_obj in name_slice_pairs:
            slices_dict[name].append(slice_obj)

        fp_inputs = (
            fp.inputs_full(strict_zero_ios)
            if (io == PortDirection.Input)
            else fp.outputs
        )
        widths = {name: reg.size for name, reg in fp_inputs.items()}
        control_names = {state.name for state in control_states}

        for name in slices_dict:
            if name in control_names:
                continue
            assert name in widths, "Name not in widths"
            if not QuantumFunctionCall._register_validate_slices(
                slices_dict[name], widths[name]
            ):
                raise ValueError(BAD_INPUT_SLICING_MSG)

    @staticmethod
    def _register_validate_slices(slices: List[slice], reg_width: int) -> bool:
        widths_separated = [len(range(reg_width)[reg_slice]) for reg_slice in slices]
        # examples: slice(0), slice(5,None) when width <= 5, slice(5,3)
        empty_slices = 0 in widths_separated

        max_stop = max(reg_slice.stop or 0 for reg_slice in slices)
        out_of_range = max_stop > reg_width

        all_widths_separated = sum(widths_separated)
        all_indices = set(
            itertools.chain.from_iterable(
                range(reg_width)[reg_slice] for reg_slice in slices
            )
        )
        all_widths_combined = len(all_indices)
        overlapping_slices = all_widths_combined != all_widths_separated

        return not any((empty_slices, out_of_range, overlapping_slices))

    @pydantic.validator("inputs")
    def _validate_inputs(
        cls, inputs: Mapping[IOName, HandleBinding], values: Dict[str, Any]
    ) -> Mapping[IOName, HandleBinding]:
        params: Optional[FunctionParams] = values.get("function_params")
        strict_zero_ios: bool = values.get("strict_zero_ios", True)
        control_states: List[ControlState] = values.get("control_states", list())
        if params is None:
            return dict()
        if isinstance(params, CustomFunction):
            if not isinstance(inputs, dict):
                raise ValueError(CUSTOM_FUNCTION_SINGLE_IO_ERROR)
            return inputs

        cls._validate_input_names(
            params=params,
            input_names=inputs.keys(),
            control_states=control_states,
            strict_zero_ios=strict_zero_ios,
        )

        cls._validate_slices(
            PortDirection.Input,
            inputs.keys(),
            params,
            strict_zero_ios,
            control_states,
        )

        return inputs

    @staticmethod
    def _validate_output_names(
        *,
        params: f_params.FunctionParams,
        output_names: Collection[IOName],
        control_states: List[ControlState],
        strict_zero_ios: bool,
    ) -> None:
        (
            invalid_expressions,
            invalid_slicings,
            invalid_names,
        ) = QuantumFunctionCall._get_invalid_ios(
            expressions=output_names,
            params=params,
            io=PortDirection.Output,
            control_states=control_states,
            strict_zero_ios=strict_zero_ios,
        )
        error_msg = []
        if invalid_expressions:
            error_msg.append(f"{BAD_OUTPUT_EXPRESSION_MSG}: {invalid_expressions}")
        if invalid_names:
            error_msg.append(f"{BAD_OUTPUT_ERROR_MSG}: {invalid_names}")
        if invalid_slicings:
            error_msg.append(f"{BAD_OUTPUT_SLICING_MSG}: {invalid_slicings}")
        if error_msg:
            raise ValueError("\n".join(error_msg))

    @pydantic.validator("outputs")
    def _validate_outputs(
        cls, outputs: Mapping[IOName, HandleBinding], values: Dict[str, Any]
    ) -> Mapping[IOName, HandleBinding]:
        params = values.get("function_params")
        strict_zero_ios: bool = values.get("strict_zero_ios", True)
        control_states = values.get("control_states", list())
        if params is None:
            return outputs
        if isinstance(params, CustomFunction):
            if not isinstance(outputs, dict):
                raise ValueError(CUSTOM_FUNCTION_SINGLE_IO_ERROR)
            return outputs

        cls._validate_output_names(
            params=params,
            output_names=outputs.keys(),
            control_states=control_states,
            strict_zero_ios=strict_zero_ios,
        )

        cls._validate_slices(
            PortDirection.Output,
            outputs.keys(),
            params,
            strict_zero_ios,
            control_states,
        )

        return outputs

    @staticmethod
    def _get_invalid_ios(
        *,
        expressions: Iterable[str],
        params: f_params.FunctionParams,
        io: f_params.PortDirection,
        control_states: List[ControlState],
        strict_zero_ios: bool,
    ) -> Tuple[List[str], List[str], List[str]]:
        expression_matches: Iterable[Optional[Match]] = map(
            functools.partial(re.fullmatch, IO_REGEX), expressions
        )

        valid_matches: List[Match] = []
        invalid_expressions: List[str] = []
        for expression, expression_match in zip(expressions, expression_matches):
            invalid_expressions.append(
                expression
            ) if expression_match is None else valid_matches.append(expression_match)

        invalid_slicings: List[str] = []
        invalid_names: List[str] = []
        valid_names = frozenset(
            params.inputs_full(strict_zero_ios)
            if io == PortDirection.Input
            else params.outputs
        )
        for match in valid_matches:
            name = match.groupdict().get(NAME)
            if name is None:
                raise AssertionError("Input/output name validation error")

            slicing = match.groupdict().get(SLICING)
            if slicing is not None and re.fullmatch(LEGAL_SLICING, slicing) is None:
                invalid_slicings.append(match.string)

            if name in valid_names:
                continue
            elif all(state.name != name for state in control_states):
                invalid_names.append(name)

        return invalid_expressions, invalid_slicings, invalid_names

    def get_param_exprs(self) -> Dict[str, Expression]:
        if isinstance(self.function_params, CustomFunction):
            return super().get_param_exprs()
        else:
            return {
                name: Expression(expr=raw_expr)
                for name, raw_expr in self.function_params
                if self.function_params.is_field_gen_param(name)
            }

    @pydantic.root_validator()
    def validate_handles(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        inputs = values.get("inputs", dict())
        outputs = values.get("outputs", dict())
        inouts = values.get("inouts", dict())

        _validate_no_duplicated_ports(inputs, outputs, inouts)
        _validate_no_duplicated_handles(inputs, outputs, inouts)
        _validate_no_mixing_sliced_and_whole_handles(inouts)

        return values


class QuantumLambdaFunction(BaseModel):
    """
    The definition of an anonymous function passed as operand to higher-level functions
    """

    rename_params: Dict[str, str] = pydantic.Field(
        default_factory=dict,
        description="Mapping of the declared param to the actual variable name used ",
    )

    body: List["QuantumFunctionCall"] = pydantic.Field(
        description="A list of function calls passed to the operator"
    )


class LambdaListComprehension(BaseModel):
    """
    Specification of a list of lambda functions iteratively
    """

    count: Expression = pydantic.Field(
        description="The number of lambda functions in the list"
    )

    index_var: str = pydantic.Field(
        description="The name of the integer variable holding the iteration index"
    )

    func: QuantumLambdaFunction = pydantic.Field(
        description="A lambda function definition replicated for index values 0 to count-1"
    )


QuantumCallable = Union[str, QuantumLambdaFunction]
QuantumOperand = Union[QuantumCallable, List[QuantumCallable], LambdaListComprehension]

QuantumFunctionCall.update_forward_refs()


def get_lambda_defs(operand: QuantumOperand) -> List[QuantumCallable]:
    if isinstance(operand, list):
        return operand
    elif isinstance(operand, LambdaListComprehension):
        return [operand.func]
    else:
        return [operand]


def _check_ports_against_declaration(
    call: QuantumFunctionCall, decl: QuantumFunctionDeclaration
) -> None:
    call_input_names = set(call.inputs.keys()) | set(call.inouts.keys())

    check_params_against_declaration(
        call_input_names,
        decl.input_set,
        call.func_name,
        should_validate_missing_params=False,
    )

    call_output_names = set(call.outputs.keys()) | set(call.inouts.keys())

    check_params_against_declaration(
        call_output_names,
        decl.output_set,
        call.func_name,
        should_validate_missing_params=False,
    )

    inout_names = {
        port.name
        for port in decl.port_declarations.values()
        if port.direction == PortDeclarationDirection.Inout
    }
    inout_params = set(call.inouts.keys())

    check_params_against_declaration(
        inout_params, inout_names, call.func_name, should_validate_missing_params=False
    )
