import pygame
from sequencer import Sequencer, Step
from event import Event
from focus_manager import FocusManager, draw_focus
from typing import Optional
from tone import Tone
from views.frame import frame
from views.editable_tone import editable_tone
from views.column import column

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

    for event in events:
        if event == Event.MoveUp:
            if not local_focus.up():
                global_focus.up()
        if event == Event.MoveDown:
            if not local_focus.down():
                global_focus.down()
        if event == Event.MoveLeft:
            if not local_focus.left():
                global_focus.left()
        if event == Event.MoveRight:
            if not local_focus.right():
                global_focus.right()

    local_focus.begin_frame()

    inner = frame(focused, screen, rect, f"Phrase {id:0>2}")

    phrase = sequencer.phrase[id]

    def set_tone(i: int):
        def fun(tone: Optional[Tone]):
            assert phrase is not None
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

    if phrase is not None:
        column(
            local_focus, screen, inner, editable_tone, 16, set_tone, get_tone, events
        )

    focused_rect = local_focus.get_focused_rect()

    if focused:
        if focused_rect is not None:
            draw_focus(screen, focused_rect)
