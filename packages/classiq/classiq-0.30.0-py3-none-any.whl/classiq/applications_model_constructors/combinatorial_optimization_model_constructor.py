import json
from typing import List, Optional

import sympy
from pyomo import environ as pyo
from pyomo.core import ConcreteModel, Constraint, Objective, Var, maximize
from pyomo.core.base.objective import ScalarObjective
from pyomo.core.expr.sympy_tools import Pyomo2SympyVisitor, PyomoSympyBimap

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import ClassicalArray, Real
from classiq.interface.generator.types.combinatorial_problem import (
    CombinatorialOptimizationStructDeclaration,
)
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_call import QuantumFunctionCall

from classiq.applications.combinatorial_optimization.combinatorial_optimization_config import (
    OptimizerConfig,
    QAOAConfig,
)

_OUTPUT_VARIABLE_NAME = "solution"


def pyomo2qmod(struct_name: str, pyo_model: ConcreteModel) -> str:
    symbols_map = PyomoSympyBimap()

    variables: List[sympy.Symbol] = []

    bounds_set = False
    lower_bound = None
    upper_bound = None

    for var_dict in pyo_model.component_objects(Var):
        for key in var_dict:
            var = Pyomo2SympyVisitor(symbols_map).walk_expression(var_dict[key])
            var.name = var.name.replace(",", "_")
            variables.append(var)
            if bounds_set:
                if lower_bound != var_dict[key].lb:
                    raise ValueError("All problem variables must agree on lower bound")
                if upper_bound != var_dict[key].ub:
                    raise ValueError("All problem variables must agree on upper bound")
            else:
                lower_bound = var_dict[key].lb
                upper_bound = var_dict[key].ub
                bounds_set = True

    constraint_exprs: List[sympy.Expr] = []

    for constraint_dict in pyo_model.component_objects(Constraint):
        for key in constraint_dict:
            constraint_exprs.append(
                Pyomo2SympyVisitor(symbols_map).walk_expression(
                    constraint_dict[key].expr
                )
            )

    pyo_objective: ScalarObjective = next(pyo_model.component_objects(Objective))
    objective_type_str = "Max" if pyo_objective.sense == maximize else "Min"
    objective_expr: sympy.Expr = Pyomo2SympyVisitor(symbols_map).walk_expression(
        pyo_objective
    )

    combi_struct_decl = {
        "name": struct_name,
        "variables": {str(variable): {"kind": "int"} for variable in variables},
        "variable_lower_bound": lower_bound,
        "variable_upper_bound": upper_bound,
        "constraints": [
            {"expr": str(constraint_expr)} for constraint_expr in constraint_exprs
        ],
        "objective_type": objective_type_str,
        "objective_function": {"expr": str(objective_expr)},
    }
    return json.dumps(combi_struct_decl, indent=2)


def construct_combi_opt_py_model(
    pyo_model: pyo.ConcreteModel,
    qaoa_config: Optional[QAOAConfig] = None,
    optimizer_config: Optional[OptimizerConfig] = None,
) -> Model:
    if qaoa_config is None:
        qaoa_config = QAOAConfig()

    if optimizer_config is None:
        optimizer_config = OptimizerConfig()

    max_iteration = 0
    if optimizer_config.max_iteration is not None:
        max_iteration = optimizer_config.max_iteration

    initial_point_expression = (
        f"{optimizer_config.initial_point}"
        if optimizer_config.initial_point is not None
        else f"compute_qaoa_initial_point(optimization_problem_to_hamiltonian(get_type(MyCombiProblem), {qaoa_config.penalty_energy}),{qaoa_config.num_layers})"
    )

    return Model(
        types=[
            CombinatorialOptimizationStructDeclaration.parse_raw(
                pyomo2qmod("MyCombiProblem", pyo_model)
            )
        ],
        functions=[
            NativeFunctionDefinition(
                name="main",
                param_decls={
                    "params_list": ClassicalArray(
                        element_type=Real(), size=qaoa_config.num_layers * 2
                    )
                },
                body=[
                    QuantumFunctionCall(
                        function="qaoa_penalty",
                        params={
                            "hamiltonian": Expression(
                                expr=f"optimization_problem_to_hamiltonian(get_type(MyCombiProblem), {qaoa_config.penalty_energy})"
                            ),
                            "params_list": Expression(expr="params_list"),
                            "num_qubits": Expression(
                                expr=f"len(get_field(optimization_problem_to_hamiltonian(get_type(MyCombiProblem), {qaoa_config.penalty_energy})[0], 'pauli'))"
                            ),
                            "is_st": Expression(expr="True"),
                        },
                    ),
                ],
            ),
        ],
        classical_execution_code=f"""
vqe_result = vqe(
    hamiltonian=optimization_problem_to_hamiltonian(get_type(MyCombiProblem), {qaoa_config.penalty_energy}),
    maximize={next(pyo_model.component_objects(Objective)).sense==maximize},
    initial_point={initial_point_expression},
    optimizer=Optimizer.{optimizer_config.opt_type},
    max_iteration={max_iteration},
    tolerance={optimizer_config.tolerance},
    step_size={optimizer_config.step_size},
    skip_compute_variance={optimizer_config.skip_compute_variance},
    alpha_cvar={optimizer_config.alpha_cvar}
)
{_OUTPUT_VARIABLE_NAME} = get_optimization_solution(get_type(MyCombiProblem), vqe_result, {qaoa_config.penalty_energy})
hamiltonian = optimization_problem_to_hamiltonian(get_type(MyCombiProblem), {qaoa_config.penalty_energy})
save({{{_OUTPUT_VARIABLE_NAME!r}: {_OUTPUT_VARIABLE_NAME}, "vqe_result": vqe_result, "hamiltonian": hamiltonian}})
""",
    )


def construct_combinatorial_optimization_model(
    pyo_model: pyo.ConcreteModel,
    qaoa_config: Optional[QAOAConfig] = None,
    optimizer_config: Optional[OptimizerConfig] = None,
) -> SerializedModel:
    model = construct_combi_opt_py_model(pyo_model, qaoa_config, optimizer_config)
    return model.get_model()
