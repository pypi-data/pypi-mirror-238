from typing import Dict, Iterable, Mapping, Union

from classiq.interface.generator.function_params import IOName, PortDirection
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.local_variable_declaration import LocalVariableDeclaration
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_statement import QuantumOperation
from classiq.interface.model.validation_handle import HandleState, ValidationHandle
from classiq.interface.model.validations.handle_validation_base import (
    HandleValidationBase,
)


def _initialize_handles_to_state(
    port_declarations: Mapping[IOName, PortDeclaration],
    local_handles: Iterable[LocalVariableDeclaration],
) -> Mapping[str, ValidationHandle]:
    handles_to_state: Dict[str, ValidationHandle] = dict()

    for port_decl in port_declarations.values():
        handles_to_state[port_decl.name] = ValidationHandle(
            initial_state=HandleState.INITIALIZED
            if port_decl.direction.includes_port_direction(PortDirection.Input)
            else HandleState.UNINITIALIZED
        )

    for local_handle in local_handles:
        handles_to_state[local_handle.name] = ValidationHandle(
            initial_state=HandleState.UNINITIALIZED
        )

    return handles_to_state


class HandleValidator(HandleValidationBase):
    def __init__(
        self,
        port_declarations: Mapping[IOName, PortDeclaration],
        local_handles: Iterable[LocalVariableDeclaration],
    ) -> None:
        super().__init__(port_declarations)
        self._port_declarations = port_declarations.values()
        self._handles_to_state = _initialize_handles_to_state(
            port_declarations, local_handles
        )

    @property
    def _validation_handles_state(self) -> Mapping[str, ValidationHandle]:
        return self._handles_to_state

    def handle_call(self, call: QuantumOperation) -> None:
        self._handle_inputs(call.wiring_inputs)
        self._handle_outputs(call.wiring_outputs)
        self._handle_inouts(call.wiring_inouts)

    def _handle_inputs(self, inputs: Mapping[str, HandleBinding]) -> None:
        for handle_binding in inputs.values():
            handle_wiring_state = self._handles_to_state[handle_binding.name]
            if handle_wiring_state.state is not HandleState.INITIALIZED:
                handle_wiring_state.append_error(
                    f"Trying to access handle {handle_binding.name!r} as input but it is in incorrect state"
                )
                continue

            handle_wiring_state.uninitialize()

    def _handle_outputs(self, outputs: Mapping[str, HandleBinding]) -> None:
        for handle_binding in outputs.values():
            handle_wiring_state = self._handles_to_state[handle_binding.name]

            if handle_wiring_state.state is not HandleState.UNINITIALIZED:
                handle_wiring_state.append_error(
                    f"Trying to access handle {handle_binding.name} as output but it is in incorrect state"
                )
                continue

            handle_wiring_state.initialize()

    def _handle_inouts(
        self, inouts: Mapping[str, Union[SlicedHandleBinding, HandleBinding]]
    ) -> None:
        sliced_handles = set()
        whole_handles = set()

        for handle_binding in inouts.values():
            handle_wiring_state = self._handles_to_state[handle_binding.name]

            if handle_wiring_state.state is not HandleState.INITIALIZED:
                handle_wiring_state.append_error(
                    f"Trying to access handle {handle_binding.name} as inout but it is in incorrect state"
                )

            if isinstance(handle_binding, SlicedHandleBinding):
                sliced_handles.add(handle_binding.name)
            else:
                whole_handles.add(handle_binding.name)

        for handle in sliced_handles & whole_handles:
            self._handles_to_state[handle].append_error(
                f"Invalid use of inout handle {handle_binding.name}, used both sliced and whole"
            )
