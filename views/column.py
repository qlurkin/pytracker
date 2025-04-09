from typing import Any, Callable
import pygame
from event import Event
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
            list[Event],
        ],
        Any,
    ],
    size: int,
    set_fun: Callable[[int], Callable[[Any], None]],
    get_fun: Callable[[int], Callable[[], Any]],
    events: list[Event],
):
    width = rect.width
    height = rect.height / size
    top = rect.top
    for i in range(size):
        rect_i = pygame.Rect((rect.left, top, width, height))
        view(focus_manager, screen, rect_i, set_fun(i), get_fun(i), events)
        top = rect_i.bottom
