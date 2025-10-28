from typing import Iterable, Sequence
import math
import numpy as np


def python_rms(seq: Iterable[float]) -> float:
    """
    Pure-python RMS calculation.
    """
    seq = list(seq)
    if not seq:
        return 0.0
    s = 0.0
    for x in seq:
        s += x * x
    mean_sq = s / len(seq)
    return math.sqrt(mean_sq)


def numpy_rms(arr: Sequence[float]) -> float:
    """
    NumPy vectorized RMS. Accepts list or ndarray.
    """
    a = np.asarray(arr, dtype=float)
    if a.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(a * a)))
