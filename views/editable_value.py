from typing import Callable, Any
import pygame
from event import Event, process_events
from focus_manager import FocusManager
from .font import draw_text


def editable_value(
    focus_manager: FocusManager,
    screen: pygame.Surface,
    rect: pygame.Rect,
    set_fun: Callable[[Any], None],
    get_fun: Callable[[], Any],
    events: list[Event],
):
    focused = focus_manager(rect)
    value = get_fun()
    if focused:

        def handler(event) -> bool:
            nonlocal value
            if event == Event.EditRight:
                value += 0.05
                set_fun(value)
                return True
            if event == Event.EditLeft:
                value -= 0.05
                set_fun(value)
                return True
            return False

        process_events(events, handler)

    draw_text(screen, f"{value:.2f}", rect)
