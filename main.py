from ads import Ads
from audio_node import an
from engine import Engine
from modulate import Modulate
from sine_oscilator import SineOscilator
from device import Device
import pygame
import pygame.midi

pygame.init()
pygame.midi.init()

FREQUENCY = 440.0  # Hz (La4)
NB_TRACKS = 8


def ui(device: Device):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("PyTracker")
    clock = pygame.time.Clock()
    engine = Engine()
    device.set_node(engine)
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    engine.add_note(
                        0,
                        an(
                            Modulate(
                                an(SineOscilator(FREQUENCY)),
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

        pygame.draw.circle(
            screen, (255, 255, 255), (400, 300), engine.get_output_sensor() * 1000
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
