import pygame
import numpy as np

from ads import Ads
from audio_node import an
from engine import Engine
from focus_manager import FocusManager, draw_focus
from modulate import Modulate
from pan import Pan
from sine_oscilator import SineOscilator
from value import Value
from views.editable_value import editable_value
from views.font import grid_rect
from views.output_monitor import output_monitor
from views.scope import scope

focus_manager = FocusManager()


def ui(
    screen: pygame.Surface,
    rect: pygame.Rect,
    events: list[pygame.Event],
    engine: Engine,
):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                focus_manager.up()
            if event.key == pygame.K_DOWN:
                focus_manager.down()
            if event.key == pygame.K_LEFT:
                focus_manager.left()
            if event.key == pygame.K_RIGHT:
                focus_manager.right()
            if event.key == pygame.K_b:
                engine.add_note(
                    5,
                    an(
                        Modulate(
                            an(Pan(an(SineOscilator(440)), an(Value(0.5)))),
                            an(Ads(0.01, 0.1, 0.8)),
                        )
                    ),
                    0.5,
                    0.5,
                )

    focus_manager.begin_frame()

    editable_value(
        focus_manager,
        screen,
        grid_rect(4, 1, (20, 20)),
        engine.set_main_level,
        engine.get_main_level,
        events,
    )

    editable_value(
        focus_manager,
        screen,
        grid_rect(4, 1, (20, 80)),
        engine.set_main_level,
        engine.get_main_level,
        events,
    )

    focused_rect = focus_manager.get_focused_rect()

    if focused_rect is not None:
        draw_focus(screen, focused_rect)

    samples = np.max(engine.get_main_graph(), axis=0)

    scope(
        screen,
        pygame.Rect(0, rect.height - 200, rect.width, 200),
        samples,
    )

    output_monitor_rect = grid_rect(5, 8)
    output_monitor_rect.topright = (rect.width - 20, 20)

    output_monitor(screen, output_monitor_rect, engine)
