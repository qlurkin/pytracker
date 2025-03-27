import pygame
import numpy as np

from engine import Engine
from focus_manager import FocusManager, draw_focus
from views.editable_value import editable_value
from views.font import GRID_HEIGHT, GRID_WIDTH
from views.output_monitor import output_monitor
from views.scope import scope

focus_manager = FocusManager()


def ui(
    screen: pygame.Surface,
    rect: pygame.Rect,
    events: list[pygame.Event],
    engine: Engine,
):
    focus_manager.begin_frame()

    editable_value(
        focus_manager,
        screen,
        pygame.Rect(20, 20, 4 * GRID_WIDTH, GRID_HEIGHT),
        engine.set_main_level,
        engine.get_main_level,
        events,
    )

    editable_value(
        focus_manager,
        screen,
        pygame.Rect(20, 80, 4 * GRID_WIDTH, GRID_HEIGHT),
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
        pygame.Rect(0, 600, 1280, 200),
        samples,
    )

    output_monitor(
        screen, pygame.Rect(1000, 0, 5 * GRID_WIDTH, 8 * (GRID_HEIGHT + 2)), engine
    )
