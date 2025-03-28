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

    half_len = len(data) // 2

    sync_indice = np.argmax(data[:half_len])

    y_scale = rect.height / 2

    data = -data * y_scale + rect.height / 2 + rect.top
    Xs = np.linspace(rect.left, rect.right + rect.width, len(data))

    if sync_indice > 0:
        data = data[sync_indice:]
        Xs = Xs[:-sync_indice]

    data = data[:half_len]
    Xs = Xs[:half_len]

    pygame.draw.lines(screen, color, False, list(zip(Xs, data)), width)
