import pygame
from focus_manager import FocusManager
from util import add
from .font import GRID_HEIGHT, draw_text, grid_rect


def frame(
    focus_manager: FocusManager,
    screen: pygame.Surface,
    rect: pygame.Rect,
    title: str,
):
    focused = focus_manager(rect)
    if focused:
        color = (255, 255, 255)
        width = 2
    else:
        color = (128, 128, 128)
        width = 1
    pygame.draw.lines(
        screen,
        (255, 255, 255),
        True,
        [
            add(rect.topleft, (0, GRID_HEIGHT / 2)),
            add(rect.topright, (0, GRID_HEIGHT / 2)),
            rect.bottomright,
            rect.bottomleft,
        ],
        width,
    )
    title_rect = grid_rect(len(title), 1)
    title_rect.midtop = rect.midtop
    pygame.draw.rect(screen, (0, 0, 0), title_rect)
    draw_text(screen, f"{title}", title_rect, color)
