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

    y_scale = rect.height / 2

    data = -data * y_scale + rect.height / 2 + rect.top
    Xs = np.linspace(rect.left, rect.right, len(data))

    pygame.draw.lines(screen, color, False, list(zip(Xs, data)), width)
