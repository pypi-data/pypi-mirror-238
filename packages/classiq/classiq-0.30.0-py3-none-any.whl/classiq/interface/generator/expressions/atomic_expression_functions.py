SUPPORTED_BUILTIN_FUNCTIONS = {"len", "sum", "print"}

SUPPORTED_ATOMIC_EXPRESSION_FUNCTIONS = {
    "hypercube_entangler_graph",
    "grid_entangler_graph",
    "optimization_problem_to_hamiltonian",
    "compute_qaoa_initial_point",
    "get_optimization_solution",
    "log_normal_finance_post_process",
    "gaussian_finance_post_process",
    "get_type",
    "struct_literal",
    "get_field",
    "molecule_problem_to_hamiltonian",
    "fock_hamiltonian_problem_to_hamiltonian",
    "molecule_ground_state_solution_post_process",
    *SUPPORTED_BUILTIN_FUNCTIONS,
}
