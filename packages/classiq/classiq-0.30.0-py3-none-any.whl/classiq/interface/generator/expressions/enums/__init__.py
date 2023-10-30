from enum import EnumMeta

from .chemistry import Element, FermionMapping
from .finance_functions import FinanceFunctionType
from .ladder_operator import LadderOperator
from .optimizers import Optimizer
from .pauli import Pauli
from .qsvm_feature_map_entanglement import QSVMFeatureMapEntanglement

BUILTIN_ENUMS = dict(filter(lambda pair: isinstance(pair[1], EnumMeta), vars().items()))
