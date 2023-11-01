from __future__ import annotations

import functools, inspect, time
import typing as tp

from jijzept.type_annotation import FixedVariables


def with_measuring_time(attr):
    def _with_measuring_time(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args = list(args)
            args += [
                v for k, v in kwargs.items() if k in inspect.signature(func).parameters
            ]
            if "system_time" in kwargs:
                s = time.time()
                ret = func(*args)
                if kwargs["system_time"] is not None:
                    setattr(kwargs["system_time"], attr, time.time() - s)
            elif "solving_time" in kwargs:
                s = time.time()
                ret = func(*args)
                if kwargs["solving_time"] is not None:
                    setattr(kwargs["solving_time"], attr, time.time() - s)
            else:
                ret = func(*args)
            return ret

        return wrapper

    return _with_measuring_time


def serialize_fixed_var(
    fixed_variables: FixedVariables
) -> tp.Dict[str, tp.Any]:
    """Serializes fixed variables.

    Args:
        fixed_variables (dict[str, dict[tuple[int, ...], int]]): obj to be serialized
    Returns:
        Dict[label, List[[index,...], [value,...]]]: serialized fixed variables
    """
    result: tp.Dict[str, tp.Any] = {}

    for deci_var, interaction_dict in fixed_variables.items():
        indices_list = []
        value_list = []
        for indices, value in interaction_dict.items():
            indices_list.append(list(indices))
            value_list.append(value)

        result[deci_var] = [indices_list, value_list]

    return result
