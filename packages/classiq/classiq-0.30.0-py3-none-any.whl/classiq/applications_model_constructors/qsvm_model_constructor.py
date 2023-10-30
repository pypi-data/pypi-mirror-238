from typing import Any, Dict, List

from classiq.interface.applications.qsvm import DataList, LabelsInt
from classiq.interface.generator.expressions.enums.pauli import Pauli
from classiq.interface.generator.expressions.enums.qsvm_feature_map_entanglement import (
    QSVMFeatureMapEntanglement,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_call import QuantumFunctionCall

from classiq.exceptions import ClassiqValueError

INVALID_FEATURE_MAP_FUNC_NAME_MSG = "Invalid feature_map_function_name, it can be bloch_sphere_feature_map or pauli_feature_map"

_OUTPUT_VARIABLE_NAME = "qsvm_results"


def _bloch_sphere_feature_map_function_params(
    bloch_feature_dimension: int,
) -> Dict[str, Expression]:
    return {"feature_dimension": Expression(expr=f"{bloch_feature_dimension}")}


def _pauli_feature_map_function_params(
    paulis: List[List[Pauli]],
    entanglement: QSVMFeatureMapEntanglement,
    alpha: int,
    reps: int,
    feature_dimension: int,
) -> Dict[str, Expression]:
    paulis_str = (
        "["
        + ",".join(
            ["[" + ",".join([str(p) for p in p_list]) + "]" for p_list in paulis]
        )
        + "]"
    )
    pauli_feature_map_params = (
        f"paulis={paulis_str}, "
        f"entanglement={entanglement}, "
        f"alpha={alpha}, "
        f"reps={reps}, "
        f"feature_dimension={feature_dimension}"
    )
    return {
        "feature_map": Expression(
            expr=f"struct_literal(QSVMFeatureMapPauli, {pauli_feature_map_params})"
        )
    }


def get_qsvm_qmain_body(
    feature_map_function_name: str, **kwargs: Any
) -> List[QuantumFunctionCall]:
    if feature_map_function_name == "bloch_sphere_feature_map":
        params = _bloch_sphere_feature_map_function_params(**kwargs)
    elif feature_map_function_name == "pauli_feature_map":
        params = _pauli_feature_map_function_params(**kwargs)
    else:
        raise ClassiqValueError(INVALID_FEATURE_MAP_FUNC_NAME_MSG)

    return [
        QuantumFunctionCall(
            function=feature_map_function_name,
            params=params,
        ),
    ]


def construct_qsvm_model(
    train_data: DataList,
    train_labels: LabelsInt,
    test_data: DataList,
    test_labels: LabelsInt,
    predict_data: DataList,
    feature_map_function_name: str,
    **kwargs: Any,
) -> SerializedModel:
    qsvm_qmod = Model(
        functions=[
            NativeFunctionDefinition(
                name="main",
                body=get_qsvm_qmain_body(
                    feature_map_function_name=feature_map_function_name, **kwargs
                ),
            ),
        ],
        classical_execution_code=f"""
{_OUTPUT_VARIABLE_NAME} = qsvm_full_run(
    train_data={train_data},
    train_labels={train_labels},
    test_data={test_data},
    test_labels={test_labels},
    predict_data={predict_data}
)
save({{{_OUTPUT_VARIABLE_NAME!r}: {_OUTPUT_VARIABLE_NAME}}})
""",
    )

    return qsvm_qmod.get_model()
