from collections.abc import Generator
from typing import Callable, NoReturn
import numpy.typing as npt
import numpy as np

AudioNode = Generator[npt.NDArray[np.float64], int, NoReturn]
AudioNodeConstructor = Callable[..., AudioNode]


def an(fun: AudioNodeConstructor, *args, **kwargs) -> AudioNode:
    node = fun(*args, **kwargs)
    next(node)
    return node
