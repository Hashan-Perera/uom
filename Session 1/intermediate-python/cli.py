"""
Optional tiny CLI using typer. If you don't have typer installed,
you can ignore this file or install via `pip install typer`.
"""
from pathlib import Path
from typing import Optional
import numpy as np
import math
import logging

logger = logging.getLogger(__name__)

try:
    import typer
except Exception:
    typer = None  # CLI not available

from .config import LabConfig
from .io import load_signal_csv, save_features_csv
from .features import feature_vector
from .vectorize import numpy_rms

def _ensure_typer():
    if typer is None:
        raise RuntimeError("typer is not installed. Install with `pip install typer`.")


def generate_synthetic(path: Path, n_samples: int = 5000, seed: Optional[int] = None):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 1, n_samples)
    signal = 0.6 * np.sin(2 * math.pi * 5 * t) + 0.3 * np.sign(np.sin(2 * math.pi * 50 * t))
    signal += rng.normal(scale=0.05, size=n_samples)
    np.savetxt(path, signal, delimiter=",")
    logger.info("Generated synthetic data to %s", path)


def run_pipeline(signal_path: Path, out_path: Path, chunk_size: int = 1024, window: int = 100):
    data = load_signal_csv(signal_path)
    rows = []
    # process in chunks to simulate streaming; compute features per chunk
    for i in range(0, data.size, chunk_size):
        chunk = data[i:i + chunk_size]
        fv = feature_vector(chunk)
        rows.append(fv)
    save_features_csv(out_path, rows)
    logger.info("Saved features to %s (chunks=%d)", out_path, len(rows))


if typer is not None:
    app = typer.Typer()

    @app.command()
    def generate_data(path: Path = Path("data/signal.csv"), samples: int = 5000, seed: int = 0):
        generate_synthetic(path, n_samples=samples, seed=seed)
        typer.echo(f"Generated {samples} samples -> {path}")

    @app.command()
    def run_pipeline_cmd(
        signal: Path = Path("data/signal.csv"),
        out: Path = Path("data/features.csv"),
        chunk_size: int = 1024,
        window: int = 100,
    ):
        run_pipeline(signal, out, chunk_size=chunk_size, window=window)
        typer.echo(f"Processed {signal} -> {out}")

    def main():
        app()
else:
    def main():
        raise RuntimeError("typer not installed")
