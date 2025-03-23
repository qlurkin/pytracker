import pygame
from focus_manager import FocusManager
from .font import draw_text


def editable_value(
    focus_manager: FocusManager,
    screen: pygame.Surface,
    rect: pygame.Rect,
    set_fun,
    get_fun,
    events: list[pygame.Event],
):
    focused = focus_manager(rect)
    value = get_fun()
    if focused:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    value += 0.05
                    set_fun(value)
                if event.key == pygame.K_o:
                    value -= 0.05
                    set_fun(value)

    draw_text(screen, f"{value:.2f}", rect)
