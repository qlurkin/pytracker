from engine import Engine
from device import Device
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


def loop(device: Device):
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("PyTracker")
    clock = pygame.time.Clock()
    engine = Engine()
    sequencer = Sequencer()
    device.set_node(engine)
    running = True
    while running:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
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
