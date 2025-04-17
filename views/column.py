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
            Callable[[], Any],
            list[Event],
        ],
        bool,
    ],
    size: int,
    set_fun: Callable[[int], Callable[[Any], None]],
    get_fun: Callable[[int], Callable[[], Any]],
    default: Callable[[], Any],
    events: list[Event],
) -> int:
    width = rect.width
    height = rect.height / size
    top = rect.top
    res = 0
    for i in range(size):
        rect_i = pygame.Rect((rect.left, top, width, height))
        if view(focus_manager, screen, rect_i, set_fun(i), get_fun(i), default, events):
            res = i
        top = rect_i.bottom
    return res
