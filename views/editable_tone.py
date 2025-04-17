from typing import Callable, Optional
import pygame
from event import Event
from focus_manager import FocusManager
from tone import Tone
from .font import draw_text


def editable_tone(
    focus_manager: FocusManager,
    screen: pygame.Surface,
    rect: pygame.Rect,
    set_fun: Callable[[Optional[Tone]], None],
    get_fun: Callable[[], Optional[Tone]],
    default: Callable[[], Tone],
    events: list[Event],
) -> bool:
    focused = focus_manager(rect)
    value: Optional[Tone] = get_fun()
    if focused:
        for event in events:
            if event == Event.EditRight:
                assert value is not None
                value.up(1)
                set_fun(value)
            if event == Event.EditLeft:
                assert value is not None
                value.down(1)
                set_fun(value)
            if event == Event.EditUp:
                assert value is not None
                value.up(12)
                set_fun(value)
            if event == Event.EditDown:
                assert value is not None
                value.down(12)
                set_fun(value)
            if event == Event.Clear:
                set_fun(None)
            if event == Event.Edit:
                if value is None:
                    value = default()
                    set_fun(value)

    if value is None:
        draw_text(screen, "---", rect)
    else:
        draw_text(screen, str(value), rect)

    return focused
