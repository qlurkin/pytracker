from ads import Ads
from audio_node import an
from modulate import Modulate
from sine_oscilator import SineOscilator
from mixer import Mixer
from engine import Engine
import pygame
import sys

FREQUENCY = 440.0  # Hz (La4)
NB_TRACKS = 8


def ui(engine: Engine):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("PyTracker")
    clock = pygame.time.Clock()
    mixer = an(Mixer(NB_TRACKS))
    engine.set_node(mixer)
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    mixer.set_track(
                        0,
                        an(
                            Modulate(
                                an(SineOscilator(FREQUENCY)), an(Ads(0.5, 0.2, 0.8))
                            )
                        ),
                    )

                if event.key == pygame.K_v:
                    mixer.set_track(1, an(SineOscilator(FREQUENCY * 0.5)))
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
