from typing import Any, Callable
import pygame
from focus_manager import FocusManager


def column(
    focus_manager: FocusManager,
    screen: pygame.Surface,
    rect: pygame.Rect,
    view: Callable[
        [
            FocusManager,
            pygame.Surface,
            pygame.Rect,
            Callable[[Any], None],
            Callable[[], Any],
            list[pygame.Event],
        ],
        Any,
    ],
    size: int,
    set_fun: Callable[[int], Callable[[Any], None]],
    get_fun: Callable[[int], Callable[[], Any]],
    events: list[pygame.Event],
):
    width = rect.width
    height = rect.height / size
    top = rect.top
    for i in range(size):
        rect_i = pygame.Rect((rect.left, top, width, height))
        view(focus_manager, screen, rect_i, set_fun(i), get_fun(i), events)
        top = rect_i.bottom
