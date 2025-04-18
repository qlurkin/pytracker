from typing import Callable, Any
import pygame
from event import Event, process_events
from focus_manager import FocusManager
from util import clamp
from .font import draw_text


def editable_byte(
    focus_manager: FocusManager,
    screen: pygame.Surface,
    rect: pygame.Rect,
    set_fun: Callable[[Any], None],
    get_fun: Callable[[], Any],
    default: Callable[[], Any],
    events: list[Event],
) -> bool:
    focused = focus_manager(rect)
    value = get_fun()
    if focused:

        def handler(event) -> bool:
            nonlocal value
            if event == Event.EditRight:
                value += 1
                value = clamp(value, 0, 255)
                set_fun(value)
                return True
            if event == Event.EditLeft:
                value -= 1
                value = clamp(value, 0, 255)
                set_fun(value)
                return True
            if event == Event.EditUp:
                value += 16
                value = clamp(value, 0, 255)
                set_fun(value)
                return True
            if event == Event.EditDown:
                value -= 16
                value = clamp(value, 0, 255)
                set_fun(value)
                return True
            if event == Event.Edit:
                if value is None:
                    value = default()
                    set_fun(value)
                return True
            return False

        process_events(events, handler)

    if value is None:
        draw_text(screen, "--", rect)
    else:
        draw_text(screen, f"{value:0>2x}", rect)

    return focused
