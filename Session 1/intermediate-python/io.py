from pathlib import Path
from typing import Iterable, Sequence, List
import numpy as np
import csv
import logging

logger = logging.getLogger(__name__)


def load_signal_csv(path: Path):
    """
    Load a one-column CSV (or whitespace separated) of signal samples into a 1D numpy array.
    Raises FileNotFoundError or ValueError on bad data.
    """
    p = Path(path)
    if not p.exists():
        logger.error("File not found: %s", p)
        raise FileNotFoundError(f"No such file: {p}")
    try:
        data = np.loadtxt(p, delimiter=",")
        # If data is 2D with one column, flatten
        if data.ndim > 1:
            data = data.flatten()
        return data.astype(float)
    except Exception as exc:
        logger.exception("Failed to load signal CSV: %s", exc)
        raise


def save_features_csv(path: Path, rows: Iterable[Sequence]):
    """
    Write features rows (iterable of sequences) to CSV path.
    Each row will be written as comma-separated floats.
    Overwrites existing file.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        with p.open("w", newline="") as fh:
            writer = csv.writer(fh)
            # header
            writer.writerow(["rms", "zero_crossings", "peak_to_peak", "mad"])
            for row in rows:
                writer.writerow([float(x) for x in row])
    except Exception as exc:
        logger.exception("Failed to save features CSV: %s", exc)
        raise
