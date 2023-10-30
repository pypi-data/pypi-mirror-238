from typing import Any, TypeVar, cast

import numpy as np


# numpy utils
def _is_empty_ndarray(obj: np.ndarray) -> bool:
    return 0 in obj.shape


def bool_datum(
    obj: Any,
) -> Any:  # returning `Any` since any object in python is convertable to `bool`
    if isinstance(obj, np.ndarray):
        # check that it's non-empty
        return not _is_empty_ndarray(obj)
    else:
        return obj


def bool_data(*objects: Any) -> bool:
    return all(map(bool_datum, objects))


T = TypeVar("T")


def choose_first(*objects: T) -> T:
    for obj in objects:
        if isinstance(obj, np.ndarray):
            if not _is_empty_ndarray(obj):
                return cast(T, obj)
        else:
            if obj:
                return obj
    # if everything failed, return the last
    return objects[-1]
