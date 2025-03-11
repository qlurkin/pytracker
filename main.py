from audio_node import an
from sine_oscilator import sine_oscilator
from mixer import mixer, set_track
from engine import Engine
import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

FREQUENCY = 440.0  # Hz (La4)

engine = Engine(an(mixer))

engine.start()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                set_track(0, an(sine_oscilator, FREQUENCY))
            if event.key == pygame.K_v:
                set_track(1, an(sine_oscilator, FREQUENCY * 0.5))
        if event.type == pygame.QUIT:
            engine.stop()
            sys.exit()

    pygame.display.flip()
