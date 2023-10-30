from math import floor, log
from typing import Union

from classiq.interface.finance.function_input import FinanceFunctionInput
from classiq.interface.finance.gaussian_model_input import GaussianModelInput
from classiq.interface.finance.log_normal_model_input import LogNormalModelInput
from classiq.interface.generator.expressions.enums.finance_functions import (
    FINANCE_FUNCTION_STRING,
    FinanceFunctionType,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import (
    QuantumFunctionCall,
    QuantumLambdaFunction,
)

from classiq.applications_model_constructors.libraries.ampltitude_estimation_library import (
    AE_CLASSICAL_LIBRARY,
)
from classiq.applications_model_constructors.libraries.qmci_library import QMCI_LIBRARY
from classiq.exceptions import ClassiqError

_OUTPUT_VARIABLE_NAME = "result"


def construct_finance_model(
    finance_model_input: Union[LogNormalModelInput, GaussianModelInput],
    finance_function_input: FinanceFunctionInput,
    phase_port_size: int,
) -> SerializedModel:
    if isinstance(finance_model_input, LogNormalModelInput):
        finance_model = f"struct_literal(LogNormalModel, num_qubits={finance_model_input.num_qubits}, mu={finance_model_input.mu}, sigma={finance_model_input.sigma})"
        finance_function = "log_normal_finance"
        post_process_function = "log_normal_finance_post_process"
        total_num_qubits = finance_model_input.num_qubits
    elif isinstance(finance_model_input, GaussianModelInput):
        finance_model = f"struct_literal(GaussianModel, num_qubits={finance_model_input.num_qubits}, normal_max_value={finance_model_input.normal_max_value}, default_probabilities={finance_model_input.default_probabilities}, rhos={finance_model_input.rhos}, loss={finance_model_input.loss}, min_loss={finance_model_input.min_loss})"
        finance_function = "gaussian_finance"
        post_process_function = "gaussian_finance_post_process"
        total_num_qubits = (
            finance_model_input.num_qubits
            + len(finance_model_input.rhos)
            + floor(log(sum(finance_model_input.loss), 2))
            + 1
        )
    else:
        raise ClassiqError(f"Invalid model input: {finance_model_input}")

    if isinstance(finance_function_input.f, FinanceFunctionType):
        finance_function_f = finance_function_input.f
    elif isinstance(finance_function_input.f, str):
        finance_function_f = FINANCE_FUNCTION_STRING[finance_function_input.f]
    else:
        finance_function_f = FinanceFunctionType(finance_function_input.f)

    polynomial_degree = 0
    if finance_function_input.polynomial_degree is not None:
        polynomial_degree = finance_function_input.polynomial_degree

    tail_probability = 0.0
    if finance_function_input.tail_probability is not None:
        tail_probability = finance_function_input.tail_probability

    finance_function_object = f"struct_literal(FinanceFunction, f={finance_function_f}, threshold={finance_function_input.condition.threshold}, larger={finance_function_input.condition.larger}, polynomial_degree={polynomial_degree}, use_chebyshev_polynomial_approximation={finance_function_input.use_chebyshev_polynomial_approximation}, tail_probability={tail_probability})"

    model = Model(
        functions=[
            *QMCI_LIBRARY,
            NativeFunctionDefinition(
                name="main",
                port_declarations={
                    "phase_port": PortDeclaration(
                        name="phase_port",
                        size=Expression(expr=f"{phase_port_size}"),
                        direction=PortDeclarationDirection.Output,
                    ),
                },
                body=[
                    QuantumFunctionCall(
                        function="qmci",
                        params={
                            "num_unitary_qubits": Expression(
                                expr=f"{total_num_qubits}+1"
                            ),
                            "num_phase_qubits": Expression(expr=f"{phase_port_size}"),
                        },
                        operands={
                            "sp_op": QuantumLambdaFunction(
                                body=[
                                    QuantumFunctionCall(
                                        function=finance_function,
                                        params={
                                            "finance_model": Expression(
                                                expr=finance_model
                                            ),
                                            "finance_function": Expression(
                                                expr=finance_function_object
                                            ),
                                        },
                                        inputs={
                                            "func_port": HandleBinding(name="reg"),
                                            "obj_port": HandleBinding(name="ind"),
                                        },
                                        outputs={
                                            "func_port": HandleBinding(name="reg"),
                                            "obj_port": HandleBinding(name="ind"),
                                        },
                                    ),
                                ],
                            ),
                        },
                        outputs={"phase_port": HandleBinding(name="phase_port")},
                    ),
                ],
            ),
        ],
        classical_execution_code=AE_CLASSICAL_LIBRARY
        + f"""
estimation = execute_amplitude_estimation({phase_port_size})
{_OUTPUT_VARIABLE_NAME} = {post_process_function}({finance_model}, {finance_function_object}, estimation)
save({{{_OUTPUT_VARIABLE_NAME!r}: {_OUTPUT_VARIABLE_NAME}}})
""",
    )
    return model.get_model()
