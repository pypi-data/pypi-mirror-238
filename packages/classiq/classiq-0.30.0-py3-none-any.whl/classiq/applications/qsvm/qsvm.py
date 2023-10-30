from typing import Any, List, Union

import numpy as np

from classiq.interface.applications.qsvm import DataList, QSVMData, QSVMPreferences

Data = Union[DataList, np.ndarray]
Labels = Union[List[Any], np.ndarray]

__all__ = [
    "QSVMData",
    "QSVMPreferences",
]


def __dir__():
    return __all__
