from ads import Ads
from audio_node import an
from hr import Hr
from modulate import Modulate
from scheduler import Scheduler
from sine_oscilator import SineOscilator
from mixer import Mixer
from device import Device
import pygame

pygame.init()

FREQUENCY = 440.0  # Hz (La4)
NB_TRACKS = 8


def ui(engine: Device):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("PyTracker")
    clock = pygame.time.Clock()
    mixer = an(Mixer(NB_TRACKS))
    scheduler = Scheduler()
    mixer.set_track(1, an(scheduler))
    engine.set_node(mixer)
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    mixer.set_track(
                        0,
                        an(
                            Modulate(
                                an(
                                    Modulate(
                                        an(SineOscilator(FREQUENCY)),
                                        an(Ads(0.01, 0.1, 0.8)),
                                    )
                                ),
                                an(Hr(0.5, 0.5)),
                            )
                        ),
                    )

                if event.key == pygame.K_v:
                    scheduler.add(an(SineOscilator(FREQUENCY * 0.5)), 1)

                if event.key == pygame.K_q:
                    running = False
            if event.type == pygame.QUIT:
                running = False

        pygame.draw.circle(screen, (255, 255, 255), (400, 300), 21)

        pygame.display.flip()


def main():
    print("PyTracker")
    engine = Device()
    print("Sound Engine Created")
    engine.start()
    print("Sound Engine Started")
    ui(engine)
    engine.stop()
    print("Sound Engine Stopped")
    pygame.quit()


if __name__ == "__main__":
    main()
