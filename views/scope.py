import pygame
import numpy as np
import numpy.typing as npt


def scope(
    screen: pygame.Surface,
    rect: pygame.Rect,
    data: npt.NDArray,
    color=(255, 255, 255),
    width=1,
):
    assert data.ndim == 1

    indices = np.where((data[:-1] < 0) & (data[1:] >= 0))[0]

    y_scale = rect.height / 2

    data = -data * y_scale + rect.height / 2 + rect.top
    Xs = np.linspace(rect.left, rect.right + rect.width, len(data))

    original_data_len = len(data)

    if len(indices) > 0 and indices[0] > 0:
        data = data[indices[0] :]
        Xs = Xs[: -indices[0]]

    data = data[: original_data_len // 2]
    Xs = Xs[: original_data_len // 2]

    pygame.draw.lines(screen, color, False, list(zip(Xs, data)), width)
