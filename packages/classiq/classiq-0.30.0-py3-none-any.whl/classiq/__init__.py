"""Classiq SDK."""
import sys

from classiq.interface._version import VERSION as _VERSION
from classiq.interface.generator.application_apis import *  # noqa: F403
from classiq.interface.generator.arith.register_user_input import (
    RegisterArithmeticInfo,
    RegisterUserInput,
)
from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.expressions.enums.pauli import Pauli
from classiq.interface.generator.functions import *  # noqa: F403
from classiq.interface.generator.functions import __all__ as _ifunc_all
from classiq.interface.generator.generated_circuit import GeneratedCircuit
from classiq.interface.ide.show import show

from classiq import (
    applications,
    builtin_functions,
    exceptions,
    execution,
    model,
    synthesis,
)
from classiq._internals import _qfunc_ext, logger
from classiq._internals.async_utils import (
    enable_jupyter_notebook,
    is_notebook as _is_notebook,
)
from classiq._internals.authentication.authentication import authenticate
from classiq._internals.client import configure
from classiq._internals.config import Configuration
from classiq._internals.help import open_help
from classiq.analyzer import Analyzer
from classiq.applications_model_constructors import *  # noqa: F403
from classiq.applications_model_constructors import (
    __all__ as _application_constructors_all,
)
from classiq.executor import (
    execute,
    execute_async,
    set_quantum_program_execution_preferences,
)
from classiq.model import *  # noqa: F403
from classiq.model import __all__ as _md_all
from classiq.pyqmod import *  # noqa: F403
from classiq.pyqmod import __all__ as _pyqmod_all
from classiq.quantum_functions import *  # noqa: F403
from classiq.quantum_functions import __all__ as _qfuncs_all
from classiq.quantum_register import *  # noqa: F403
from classiq.quantum_register import __all__ as _qregs_all
from classiq.synthesis import (
    set_constraints,
    set_execution_preferences,
    set_preferences,
    synthesize,
    synthesize_async,
)

__version__ = _VERSION

if _is_notebook():
    enable_jupyter_notebook()

_sub_modules = [
    "analyzer",
    "applications",
    "builtin_functions",
    "exceptions",
    "execution",
    "model",
    "open_help",
    "pyqmod",
    "synthesis",
]

__all__ = (
    [
        "RegisterUserInput",
        "RegisterArithmeticInfo",
        "ControlState",
        "Analyzer",
        "GeneratedCircuit",
        "authenticate",
        "synthesize",
        "synthesize_async",
        "execute",
        "execute_async",
        "set_preferences",
        "set_constraints",
        "set_execution_preferences",
        "set_quantum_program_execution_preferences",
        "show",
        "Pauli",
    ]
    + _qregs_all
    + _qfuncs_all
    + _md_all
    + _ifunc_all
    + _sub_modules
    + _application_constructors_all
    + _pyqmod_all
)


def __dir__():
    return __all__
