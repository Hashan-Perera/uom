import time
import logging
from contextlib import contextmanager
from typing import ContextManager, Iterable, Type

logger = logging.getLogger(__name__)


@contextmanager
def timer(label: str = ""):
    """
    Context manager measuring time elapsed inside the block.
    Yields the elapsed time in seconds when exiting (useful for tests/logging).
    Example:
        with timer("step") as elapsed:
            ... # do work
        # elapsed contains seconds
    """
    start = time.perf_counter()
    try:
        yield lambda: time.perf_counter() - start
    finally:
        elapsed = time.perf_counter() - start
        if label:
            logger.debug("Timer [%s] elapsed: %.6f s", label, elapsed)
        # nothing returned — tests may call the yielded callable to get elapsed


@contextmanager
def suppress_and_log(*exc_types: Type[BaseException]):
    """
    Context manager that suppresses specified exceptions and logs them.
    Usage:
        with suppress_and_log(ValueError):
            ...
    """
    try:
        yield
    except exc_types as exc:
        logger.exception("Suppressed exception: %s", exc)
