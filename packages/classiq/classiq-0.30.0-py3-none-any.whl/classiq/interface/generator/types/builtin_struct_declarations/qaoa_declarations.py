from classiq.interface.generator.functions.classical_function_declaration import (
    ClassicalFunctionDeclaration,
)
from classiq.interface.generator.functions.classical_type import (
    ClassicalList,
    Integer,
    Real,
    Struct,
)
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict

COMPUTE_QAOA_INITIAL_POINT = ClassicalFunctionDeclaration(
    name="compute_qaoa_initial_point",
    param_decls={
        "hamiltonian": ClassicalList(element_type=Struct(name="PauliTerm")),
        "repetitions": Integer(),
    },
    return_type=ClassicalList(element_type=Real()),
)

ClassicalFunctionDeclaration.FOREIGN_FUNCTION_DECLARATIONS.update(
    nameables_to_dict([COMPUTE_QAOA_INITIAL_POINT])
)
