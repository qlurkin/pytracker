from ads import Ads
from audio_node import an
from engine import Engine
from modulate import Modulate
from pan import Pan
from sine_oscilator import SineOscilator
from device import Device
from focus_manager import FocusManager
import pygame
import pygame.midi
from ui import ui
from value import Value

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
    device.set_node(engine)
    focus_manager = FocusManager()
    running = True
    while running:
        clock.tick(60)
        events = pygame.event.get()
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
                                an(Pan(an(SineOscilator(FREQUENCY)), an(Value(0.5)))),
                                an(Ads(0.01, 0.1, 0.8)),
                            )
                        ),
                        0.5,
                        0.5,
                    )

                if event.key == pygame.K_q:
                    running = False
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        ui(screen, pygame.Rect((0, 0), SIZE), events, engine)

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
