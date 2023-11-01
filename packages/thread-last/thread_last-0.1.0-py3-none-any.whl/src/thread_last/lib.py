import functools
from typing import Any, Callable


def thread_last(x: Any, *fns: Callable[[Any], Any]) -> Any:
    return functools.reduce(lambda v, f: f(v), fns, x)
