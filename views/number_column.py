import pygame
from .font import draw_text


def number_column(
    screen: pygame.Surface,
    rect: pygame.Rect,
    size: int,
    width: int,
    color=(128, 128, 128),
    offset=0,
):
    height = rect.height / size
    top = rect.top
    for i in range(size):
        rect_i = pygame.Rect((rect.left, top, rect.width, height))

        draw_text(
            screen,
            ("{:0>" + str(width) + "x}").format(i + offset).upper(),
            rect_i,
            color,
        )

        top = rect_i.bottom
