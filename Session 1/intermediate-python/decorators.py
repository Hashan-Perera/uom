import time
import logging
from functools import wraps
from typing import Callable, Optional, TypeVar, Any

logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Any])


def timed(threshold_ms: Optional[int] = None):
    """
    Decorator which logs execution time. If threshold_ms provided,
    logs a WARNING when runtime exceeds threshold_ms.
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = (time.perf_counter() - start) * 1000.0  # ms
                msg = f"Function {func.__name__} took {elapsed:.2f} ms"
                if threshold_ms is not None and elapsed > threshold_ms:
                    logger.warning("%s — exceeds threshold %d ms", msg, threshold_ms)
                else:
                    logger.debug(msg)
        return wrapper  # type: ignore
    return decorator
