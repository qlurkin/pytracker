import pygame
from clipboard import ClipBoard
from sequencer import Phrase, Sequencer, Step
from event import Event, process_events
from focus_manager import FocusManager, draw_focus
from typing import Optional
from tone import Tone
from views.cursor_column import cursor_column
from views.font import draw_text, grid_rect
from views.frame import frame
from views.editable_tone import editable_tone
from views.column import column
from views.number_column import number_column

local_focus = FocusManager()


def phrase_view(
    global_focus: FocusManager,
    screen: pygame.Surface,
    rect: pygame.Rect,
    sequencer: Sequencer,
    id: int,
    events: list[Event],
):
    focused = global_focus(rect)
    if not focused:
        events = []
    else:
        if sequencer.phrase[id] is None:
            sequencer.phrase[id] = Phrase()

    def handler(event) -> bool:
        if event == Event.MoveUp:
            if not local_focus.up():
                global_focus.up()
            return True
        if event == Event.MoveDown:
            if not local_focus.down():
                global_focus.down()
            return True
        if event == Event.MoveLeft:
            if not local_focus.left():
                global_focus.left()
            return True
        if event == Event.MoveRight:
            if not local_focus.right():
                global_focus.right()
            return True
        return False

    process_events(events, handler)

    local_focus.begin_frame()

    inner = frame(focused, screen, rect, f"Phrase {id:0>2x}")

    phrase = sequencer.phrase[id]

    def default() -> Tone:
        return ClipBoard.tone

    def set_tone(i: int):
        def fun(tone: Optional[Tone]):
            assert phrase is not None
            if tone is not None:
                ClipBoard.tone = tone
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
            assert phrase is not None
            step = phrase[i]
            if step is None:
                return None
            return step.get_tone()

        return fun

    phrase_cursor = sequencer.player.get_phrase_cursor()

    def cursor_here(i: int) -> bool:
        if (id, i) in phrase_cursor:
            return True
        return False

    if phrase is not None:
        number_column_rect = grid_rect(1, 16)
        number_column_rect.topleft = inner.topleft
        number_column(screen, number_column_rect, 16, 1)
        cursor_column_rect = grid_rect(1, 16)
        cursor_column_rect.topleft = number_column_rect.topright
        cursor_column(screen, cursor_column_rect, cursor_here, 16)
        tone_column_rect = grid_rect(3, 16)
        tone_column_rect.topleft = cursor_column_rect.topright
        column(
            local_focus,
            screen,
            tone_column_rect,
            editable_tone,
            16,
            set_tone,
            get_tone,
            default,
            events,
        )

    else:
        draw_text(screen, "NONE", inner)

    focused_rect = local_focus.get_focused_rect()

    if focused:
        if focused_rect is not None:
            draw_focus(screen, focused_rect)
