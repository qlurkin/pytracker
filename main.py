from audio_node import an
from sine_oscilator import sine_oscilator
from mixer import Mixer
from engine import Engine
import pygame
import sys

FREQUENCY = 440.0  # Hz (La4)


def ui(engine: Engine):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("PyTracker")
    clock = pygame.time.Clock()
    mixer = an(Mixer)
    engine.set_node(mixer)
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    mixer.set_track(0, an(sine_oscilator, FREQUENCY))
                if event.key == pygame.K_v:
                    mixer.set_track(1, an(sine_oscilator, FREQUENCY * 0.5))
            if event.type == pygame.QUIT:
                engine.stop()
                sys.exit()

        pygame.draw.circle(screen, (255, 255, 255), (400, 300), 21)

        pygame.display.flip()


def main():
    engine = Engine()
    engine.start()
    ui(engine)
    engine.stop()


if __name__ == "__main__":
    main()
