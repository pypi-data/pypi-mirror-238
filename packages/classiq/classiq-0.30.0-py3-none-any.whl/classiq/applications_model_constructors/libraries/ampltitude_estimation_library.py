AE_CLASSICAL_LIBRARY = """
def execute_amplitude_estimation(phase_port_size):
    result = sample()
    estimation = qae_with_qpe_result_post_processing(
        estimation_register_size=phase_port_size,
        estimation_method=1,
        result=result
    )
    save({"result": result, "estimation": estimation})
    return estimation
"""
