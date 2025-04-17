from typing import Callable, Any
import pygame
from event import Event
from focus_manager import FocusManager
from util import clamp
from .font import draw_text


def editable_byte(
    focus_manager: FocusManager,
    screen: pygame.Surface,
    rect: pygame.Rect,
    set_fun: Callable[[Any], None],
    get_fun: Callable[[], Any],
    events: list[Event],
) -> bool:
    focused = focus_manager(rect)
    value = get_fun()
    if focused:
        for event in events:
            if event == Event.EditRight:
                value += 1
                value = clamp(value, 0, 255)
                set_fun(value)
            if event == Event.EditLeft:
                value -= 1
                value = clamp(value, 0, 255)
                set_fun(value)
            if event == Event.EditUp:
                value += 16
                value = clamp(value, 0, 255)
                set_fun(value)
            if event == Event.EditDown:
                value -= 16
                value = clamp(value, 0, 255)
                set_fun(value)
            if event == Event.Edit:
                if value is None:
                    value = 0
                    set_fun(value)

    if value is None:
        draw_text(screen, "--", rect)
    else:
        draw_text(screen, f"{value:0>2x}", rect)

    return focused
