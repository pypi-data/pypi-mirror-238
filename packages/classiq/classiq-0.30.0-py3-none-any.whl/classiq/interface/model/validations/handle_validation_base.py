import abc
from typing import Dict, Mapping, Type

from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.validation_handle import HandleState, ValidationHandle

EXPECTED_TERMINAL_STATES: Dict[PortDeclarationDirection, HandleState] = {
    PortDeclarationDirection.Output: HandleState.INITIALIZED,
    PortDeclarationDirection.Inout: HandleState.INITIALIZED,
}


class HandleValidationBase(abc.ABC):
    def __init__(
        self,
        port_declarations: Mapping[IOName, PortDeclaration],
    ) -> None:
        self._port_declarations = port_declarations.values()

    def report_errored_handles(self, exception_type: Type[Exception]) -> None:
        self._validate_terminal_handle_state()

        errored_handles = {
            name: state.errors
            for name, state in self._validation_handles_state.items()
            if state.state is HandleState.ERRORED
        }
        if errored_handles:
            raise exception_type(
                "\n".join(
                    f"Handle {handle_name!r} was errored with {'. '.join(errors)!r}"
                    for handle_name, errors in errored_handles.items()
                )
            )

    def _validate_terminal_handle_state(self) -> None:
        for port_decl in self._port_declarations:
            handle_state = self._validation_handles_state[port_decl.name]
            expected_terminal_state = EXPECTED_TERMINAL_STATES.get(port_decl.direction)
            if (
                expected_terminal_state is not None
                and handle_state.state is not expected_terminal_state
                and handle_state.state is not HandleState.ERRORED
            ):
                handle_state.append_error(
                    f"At the end of the function, in port {port_decl.name} is expected to be {expected_terminal_state} but it isn't"
                )

    @property
    @abc.abstractmethod
    def _validation_handles_state(self) -> Mapping[str, ValidationHandle]:
        raise NotImplementedError
