from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class LabConfig:
    """
    Frozen dataclass holding configuration for the lab.
    Use LabConfig() to get sensible defaults.
    """
    data_dir: Path = Path("data")
    signal_csv: Path = Path("data/signal.csv")
    features_csv: Path = Path("data/features.csv")
    chunk_size: int = 1024
    moving_window: int = 5
    verbose: bool = False
    # optional: threshold for timed decorator reporting (ms)
    slow_threshold_ms: Optional[int] = None
