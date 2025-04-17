from typing import Callable, Optional
import pygame
from event import Event
from focus_manager import FocusManager
from tone import Tone
from .font import draw_text
from clipboard import ClipBoard


def editable_tone(
    focus_manager: FocusManager,
    screen: pygame.Surface,
    rect: pygame.Rect,
    set_fun: Callable[[Optional[Tone]], None],
    get_fun: Callable[[], Optional[Tone]],
    events: list[Event],
) -> bool:
    focused = focus_manager(rect)
    value: Optional[Tone] = get_fun()
    if focused:
        for event in events:
            if event == Event.EditRight:
                if value is None:
                    value = ClipBoard.tone
                value.up(1)
                set_fun(value)
                ClipBoard.tone = value
            if event == Event.EditLeft:
                if value is None:
                    value = ClipBoard.tone
                value.down(1)
                set_fun(value)
                ClipBoard.tone = value
            if event == Event.EditUp:
                if value is None:
                    value = ClipBoard.tone
                value.up(12)
                set_fun(value)
                ClipBoard.tone = value
            if event == Event.EditDown:
                if value is None:
                    value = ClipBoard.tone
                value.down(12)
                set_fun(value)
                ClipBoard.tone = value
            if event == Event.Clear:
                set_fun(None)
            if event == Event.Edit:
                if value is None:
                    value = ClipBoard.tone
                    set_fun(value)

    if value is None:
        draw_text(screen, "---", rect)
    else:
        draw_text(screen, str(value), rect)

    return focused
