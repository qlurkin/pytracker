from typing import Callable
import pygame
from .font import draw_text


def cursor_column(
    screen: pygame.Surface,
    rect: pygame.Rect,
    get_fun: Callable[[int], bool],
    size: int,
):
    width = rect.width
    height = rect.height / size
    top = rect.top
    for i in range(size):
        rect_i = pygame.Rect((rect.left, top, width, height))
        value = get_fun(i)

        if value:
            draw_text(screen, "▹", rect_i)

        top = rect_i.bottom
