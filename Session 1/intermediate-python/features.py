import numpy as np
from .vectorize import numpy_rms
from typing import Sequence, List


def zero_crossings(x: np.ndarray) -> int:
    """Count number of times the signal crosses zero (sign change)."""
    if x.size == 0:
        return 0
    s = np.sign(x)
    # treat zeros as previous sign to avoid extra crossings
    s[s == 0] = 1
    crossings = np.where(np.diff(s) != 0)[0]
    return int(crossings.size)


def peak_to_peak(x: np.ndarray) -> float:
    if x.size == 0:
        return 0.0
    return float(np.max(x) - np.min(x))


def mad(x: np.ndarray) -> float:
    """Mean absolute deviation about the mean."""
    if x.size == 0:
        return 0.0
    return float(np.mean(np.abs(x - np.mean(x))))


def feature_vector(x: Sequence[float]) -> List[float]:
    """
    Compute [rms, zero_crossings, peak_to_peak, mad] for a 1-D sequence.
    Returns a list of floats/ints.
    """
    arr = np.asarray(x, dtype=float)
    r = numpy_rms(arr)
    zc = zero_crossings(arr)
    p2p = peak_to_peak(arr)
    m = mad(arr)
    return [r, float(zc), p2p, m]
