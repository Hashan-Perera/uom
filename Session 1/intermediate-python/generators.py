from collections import deque
from typing import Iterable, Iterator, List, Deque, Optional
import bisect
import logging
logger = logging.getLogger(__name__)


def chunks(iterable: Iterable, size: int) -> Iterator[List]:
    """
    Yield lists of length up to `size` from `iterable`.
    Example: list(chunks(range(7), 3)) -> [[0,1,2],[3,4,5],[6]]
    """
    if size <= 0:
        raise ValueError("size must be > 0")
    it = iter(iterable)
    batch = []
    for item in it:
        batch.append(item)
        if len(batch) >= size:
            logger.debug("Yielding chunk of size %d", len(batch))
            yield batch
            batch = []
    if batch:
        logger.debug("Yielding final chunk of size %d", len(batch))
        yield batch


def moving_average(window: int):
    """
    Generator-style coroutine that accepts values via .send(x)
    and yields the current moving average after each .send.
    Must be primed by calling next(gen) before sending the first value.
    """
    if window <= 0:
        raise ValueError("window must be > 0")
    dq: Deque[float] = deque()
    s = 0.0
    try:
        while True:
            x = yield (s / len(dq)) if dq else 0.0
            # accept values: if generator receives None via next(), it yields current average without updating
            if x is None:
                continue
            dq.append(x)
            s += x
            if len(dq) > window:
                s -= dq.popleft()
            avg = s / len(dq)
            logger.debug("Moving average window=%d avg=%.6f", window, avg)
    except GeneratorExit:
        return


def moving_median(window: int):
    """
    Stateful coroutine for moving median. Use .send(value) to push values.
    Prime with next(gen) before sending.
    Maintains a sorted list for median and a deque for order.
    """
    if window <= 0:
        raise ValueError("window must be > 0")
    order: Deque[float] = deque()
    sorted_list: list = []
    try:
        while True:
            _ = yield (sorted_list[len(sorted_list)//2] if sorted_list else 0.0)
            x = _
            if x is None:
                continue
            order.append(x)
            bisect.insort(sorted_list, x)
            if len(order) > window:
                old = order.popleft()
                # remove old from sorted_list
                idx = bisect.bisect_left(sorted_list, old)
                if 0 <= idx < len(sorted_list):
                    sorted_list.pop(idx)
            # median:
            n = len(sorted_list)
            if n == 0:
                med = 0.0
            elif n % 2 == 1:
                med = float(sorted_list[n // 2])
            else:
                med = (sorted_list[n // 2 - 1] + sorted_list[n // 2]) / 2.0
            logger.debug("Moving median window=%d median=%.6f", window, med)
    except GeneratorExit:
        return
