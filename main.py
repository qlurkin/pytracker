from ads import Ads
from audio_node import an
from engine import Engine
from modulate import Modulate
from pan import Pan
from sine_oscilator import SineOscilator
from device import Device
from focus_manager import FocusManager, draw_focus
import pygame
import pygame.midi
from value import Value
from views.editable_value import editable_value
from views.font import GRID_HEIGHT, GRID_WIDTH

pygame.init()
pygame.midi.init()


FREQUENCY = 440.0  # Hz (La4)
NB_TRACKS = 8


def ui(device: Device):
    screen = pygame.display.set_mode((1280, 800))
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
                        0,
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
            # pygame.draw.rect(screen, (255, 255, 0), focused_rect)
            draw_focus(screen, focused_rect)

        pygame.draw.circle(
            screen, (255, 255, 255), (400, 300), max(engine.get_output_sensor()) * 1000
        )

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
    print("PyTracker")
    print_midi_device_info()
    engine = Device()
    print("Sound Engine Created")
    engine.start()
    print("Sound Engine Started")
    ui(engine)
    engine.stop()
    print("Sound Engine Stopped")
    pygame.midi.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
