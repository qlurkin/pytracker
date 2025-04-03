from typing import Optional
import pygame
import numpy as np

from ads import Ads
from audio_node import an
from engine import Engine
from focus_manager import FocusManager, draw_focus
from modulate import Modulate
from pan import Pan
from sequencer import Sequencer, Step
from sine_oscilator import SineOscilator
from tone import Tone
from value import Value
from views.column import column
from views.editable_tone import editable_tone
from views.frame import frame
from views.editable_value import editable_value
from views.font import GRID_HEIGHT, draw_text, grid_rect
from views.output_monitor import output_monitor
from views.scope import scope

focus_manager = FocusManager()


def ui(
    screen: pygame.Surface,
    rect: pygame.Rect,
    events: list[pygame.Event],
    engine: Engine,
    sequencer: Sequencer,
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
            if event.key == pygame.K_v:
                engine.add_note(
                    3,
                    an(
                        Modulate(
                            an(
                                Pan(
                                    an(SineOscilator(Tone(6, 4).frequency)),
                                    an(Value(0.5)),
                                )
                            ),
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

    editable_value(
        focus_manager,
        screen,
        grid_rect(4, 1, (20, tempo_rect.top)),
        engine.set_main_level,
        engine.get_main_level,
        events,
    )

    editable_value(
        focus_manager,
        screen,
        grid_rect(4, 1, (20, tempo_rect.top + GRID_HEIGHT)),
        engine.set_main_level,
        engine.get_main_level,
        events,
    )

    draw_text(
        screen,
        str(sequencer.step_count),
        grid_rect(10, 1, (20, tempo_rect.top + 2 * GRID_HEIGHT)),
    )

    inner = frame(
        focus_manager, screen, pygame.Rect(200, 200, 300, 16 * GRID_HEIGHT), "Phrase"
    )

    phrase = sequencer.phrase[0]
    assert phrase is not None

    def set_tone(i: int):
        def fun(tone: Optional[Tone]):
            if tone is None:
                phrase[i] = None
                return
            step = phrase[i]
            if step is None:
                step = Step(tone)
                step.set_instrument(0)
                phrase[i] = step
            else:
                step.set_tone(tone)

        return fun

    def get_tone(i: int):
        def fun() -> Optional[Tone]:
            step = phrase[i]
            if step is None:
                return None
            return step.get_tone()

        return fun

    column(focus_manager, screen, inner, editable_tone, 16, set_tone, get_tone, events)

    focused_rect = focus_manager.get_focused_rect()

    if focused_rect is not None:
        draw_focus(screen, focused_rect)
