import pygame
import numpy as np

from ads import Ads
from audio_node import an
from engine import Engine
from event import Event
from focus_manager import FocusManager
from modulate import Modulate
from pan import Pan
from sequencer import Sequencer
from sine_oscilator import SineOscilator
from value import Value
from views.chain_view import chain_view
from views.font import GRID_HEIGHT, draw_text, grid_rect
from views.output_monitor import output_monitor
from views.phrase_view import phrase_view
from views.scope import scope

focus_manager = FocusManager()


def ui(
    screen: pygame.Surface,
    rect: pygame.Rect,
    events: list[Event],
    engine: Engine,
    sequencer: Sequencer,
):
    for event in events:
        if event == Event.ShiftMoveUp:
            focus_manager.up()
        if event == Event.ShiftMoveDown:
            focus_manager.down()
        if event == Event.ShiftMoveLeft:
            focus_manager.left()
        if event == Event.ShiftMoveRight:
            focus_manager.right()
        if event == Event.Play:
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

    samples = np.max(engine.get_main_graph(), axis=0)

    scope_rect = pygame.Rect(0, 0, rect.width, 150)

    scope(screen, scope_rect, samples)

    tempo_rect = grid_rect(5, 1)
    tempo_rect.topright = (rect.width - 20, scope_rect.bottom + 20)
    draw_text(screen, f"T▹{sequencer.get_tempo()}", tempo_rect)

    output_monitor_rect = grid_rect(5, 8)
    output_monitor_rect.topright = tempo_rect.bottomright

    output_monitor(screen, output_monitor_rect, engine)

    chain_view(
        focus_manager,
        screen,
        pygame.Rect(0, 200, 300, 16 * GRID_HEIGHT),
        sequencer,
        0,
        events,
    )

    phrase_view(
        focus_manager,
        screen,
        pygame.Rect(300, 200, 300, 16 * GRID_HEIGHT),
        sequencer,
        0,
        events,
    )
