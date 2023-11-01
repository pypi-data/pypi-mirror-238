from __future__ import annotations

import typing as tp

import numpy as np

InstanceDataValue = tp.Union[int, float, np.integer, np.floating, np.ndarray, list]
InstanceData = tp.Dict[str, InstanceDataValue]

FixedVariables = tp.Dict[str, tp.Dict[tp.Tuple[int, ...], int]]