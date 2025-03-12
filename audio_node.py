from collections.abc import Generator
from typing import NoReturn, TypeVar
import numpy.typing as npt
import numpy as np


AudioNode = Generator[npt.NDArray[np.floating], int, NoReturn]

T = TypeVar("T", bound=AudioNode)


def an(node: T, *args, **kwargs) -> T:
    next(node)
    return node
