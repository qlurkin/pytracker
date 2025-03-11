from collections.abc import Generator
from typing import Callable, NoReturn, TypeVar
import numpy.typing as npt
import numpy as np


AudioNode = Generator[npt.NDArray[np.float64], int, NoReturn]

T = TypeVar("T", bound=AudioNode)


def an(fun: Callable[..., T], *args, **kwargs) -> T:
    node = fun(*args, **kwargs)
    next(node)
    return node
