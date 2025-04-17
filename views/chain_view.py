import pygame
from clipboard import ClipBoard
from sequencer import Sequencer
from event import Event
from focus_manager import FocusManager, draw_focus
from typing import Optional
from views.editable_byte import editable_byte
from views.font import draw_text
from views.frame import frame
from views.column import column
import views.ui as ui

local_focus = FocusManager()


def chain_view(
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

    inner = frame(focused, screen, rect, f"Chain {id:0>2}")

    chain = sequencer.chain[id]

    def default() -> int:
        return ClipBoard.phrase_id

    def set_phrase(i: int):
        def fun(phrase_id: Optional[int]):
            assert chain is not None
            chain[i] = phrase_id
            if phrase_id is not None:
                ClipBoard.phrase_id = phrase_id

        return fun

    def get_phrase(i: int):
        def fun() -> Optional[int]:
            assert chain is not None
            return chain[i]

        return fun

    if chain is not None:
        focused_slot = column(
            local_focus,
            screen,
            inner,
            editable_byte,
            16,
            set_phrase,
            get_phrase,
            default,
            events,
        )

        phrase_id = chain[focused_slot]
        if phrase_id is not None:
            ui.ui_state.phrase_id = phrase_id
    else:
        draw_text(screen, "NONE", inner)

    focused_rect = local_focus.get_focused_rect()

    if focused:
        if focused_rect is not None:
            draw_focus(screen, focused_rect)
