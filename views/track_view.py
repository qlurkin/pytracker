import pygame
from clipboard import ClipBoard
from sequencer import Sequencer
from event import Event
from focus_manager import FocusManager, draw_focus
from typing import Optional
from views.cursor_column import cursor_column
from views.editable_byte import editable_byte
from views.font import grid_rect
from views.column import column
import views.ui as ui

local_focus = FocusManager()


def track_view(
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

    track = sequencer.track[id]

    def default() -> int:
        return ClipBoard.chain_id

    def set_chain(i: int):
        def fun(chain_id: Optional[int]):
            assert track is not None
            track[i] = chain_id
            if chain_id is not None:
                ClipBoard.chain_id = chain_id

        return fun

    def get_phrase(i: int):
        def fun() -> Optional[int]:
            assert track is not None
            return track[i]

        return fun

    track_cursor = sequencer.player.get_track_cursor()

    def cursor_here(i: int) -> bool:
        if (id, i) in track_cursor:
            return True
        return False

    cursor_column_rect = grid_rect(1, 16)
    cursor_column_rect.topleft = rect.topleft
    cursor_column(screen, cursor_column_rect, cursor_here, 16)
    phrase_rect = grid_rect(2, 16)
    phrase_rect.topleft = cursor_column_rect.topright
    focused_slot = column(
        local_focus,
        screen,
        phrase_rect,
        editable_byte,
        16,
        set_chain,
        get_phrase,
        default,
        events,
    )

    chain_id = track[focused_slot]
    if chain_id is not None:
        ui.ui_state.chain_id = chain_id

    focused_rect = local_focus.get_focused_rect()

    if focused:
        if focused_rect is not None:
            draw_focus(screen, focused_rect)
