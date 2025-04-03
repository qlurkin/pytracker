from typing import Callable, Optional
import pygame
from focus_manager import FocusManager
from tone import Tone
from .font import draw_text


def editable_tone(
    focus_manager: FocusManager,
    screen: pygame.Surface,
    rect: pygame.Rect,
    set_fun: Callable[[Optional[Tone]], None],
    get_fun: Callable[[], Optional[Tone]],
    events: list[pygame.Event],
):
    focused = focus_manager(rect)
    value: Optional[Tone] = get_fun()
    if focused:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if value is None:
                        value = Tone()
                    value.up(1)
                    set_fun(value)
                if event.key == pygame.K_o:
                    if value is None:
                        value = Tone()
                    value.down(1)
                    set_fun(value)

    if value is None:
        draw_text(screen, "---", rect)
    else:
        draw_text(screen, str(value), rect)
