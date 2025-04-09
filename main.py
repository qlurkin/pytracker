from engine import Engine
from device import Device
from event import Event, Key
from sequencer import Sequencer
import pygame
import pygame.midi
from views.ui import ui

pygame.init()
pygame.midi.init()


FREQUENCY = 440
NB_TRACKS = 8
WIDTH = 1280
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)


KEYMAP = {
    pygame.K_UP: Key.Up,
    pygame.K_DOWN: Key.Down,
    pygame.K_LEFT: Key.Left,
    pygame.K_RIGHT: Key.Right,
    pygame.K_z: Key.Edit,
    pygame.K_x: Key.Option,
    pygame.K_c: Key.Shift,
    pygame.K_v: Key.Play,
}

NO_HELD_EVENTS = {
    Key.Up: Event.MoveUp,
    Key.Down: Event.MoveDown,
    Key.Left: Event.MoveLeft,
    Key.Right: Event.MoveRight,
    Key.Edit: Event.Edit,
    Key.Play: Event.Play,
}

SHIFT_EVENTS = {
    Key.Up: Event.ShiftMoveUp,
    Key.Down: Event.ShiftMoveDown,
    Key.Left: Event.ShiftMoveLeft,
    Key.Right: Event.ShiftMoveRight,
    Key.Play: Event.ShiftPlay,
}

EDIT_EVENTS = {
    Key.Up: Event.EditUp,
    Key.Down: Event.EditDown,
    Key.Left: Event.EditLeft,
    Key.Right: Event.EditRight,
}

OPTION_EVENTS = {
    Key.Edit: Event.Clear,
}


def loop(device: Device):
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("PyTracker")
    clock = pygame.time.Clock()
    engine = Engine()
    sequencer = Sequencer(engine)
    device.set_node(engine)
    running = True
    held = set()
    while running:
        clock.tick(60)
        events = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key in KEYMAP:
                    key = KEYMAP[event.key]
                    if len(held) == 0:
                        if key in NO_HELD_EVENTS:
                            events.append(NO_HELD_EVENTS[key])
                    elif Key.Shift in held:
                        if key in SHIFT_EVENTS:
                            events.append(SHIFT_EVENTS[key])
                    elif Key.Edit in held:
                        if key in EDIT_EVENTS:
                            events.append(EDIT_EVENTS[key])
                    elif Key.Option in held:
                        if key in OPTION_EVENTS:
                            events.append(OPTION_EVENTS[key])

                    held.add(key)
            if event.type == pygame.KEYUP:
                if event.key in KEYMAP:
                    key = KEYMAP[event.key]
                    held.remove(key)

            if event.type == pygame.QUIT:
                running = False

        sequencer.update()
        screen.fill((0, 0, 0))

        ui(screen, pygame.Rect((0, 0), SIZE), events, engine, sequencer)

        pygame.display.flip()


def print_midi_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )


def main():
    print_midi_device_info()
    engine = Device()
    engine.start()
    loop(engine)
    engine.stop()
    pygame.midi.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
