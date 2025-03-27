import pygame
import numpy as np

from engine import Engine
from config import NB_TRACKS
from tone import tone_to_str
from util import freq_to_tone, get_freq
from views.font import GRID_HEIGHT, draw_text, grid_rect


def output_monitor(screen: pygame.Surface, rect: pygame.Rect, engine: Engine):
    main_sensor_factor = rect.width * 5 / 6
    main_sensor = engine.get_main_sensor()
    main_sensor_left = main_sensor[0] * main_sensor_factor
    main_sensor_right = main_sensor[1] * main_sensor_factor
    main_monitor_left_rect = pygame.Rect(
        rect.left, rect.top, main_sensor_left, GRID_HEIGHT // 2 - 2
    )
    main_monitor_right_rect = pygame.Rect(
        rect.left,
        main_monitor_left_rect.bottom + 2,
        main_sensor_right,
        main_monitor_left_rect.height,
    )

    pygame.draw.rect(screen, (255, 255, 255), main_monitor_left_rect)
    pygame.draw.rect(screen, (255, 255, 255), main_monitor_right_rect)

    track_rect = grid_rect(5, 1)
    track_rect.topleft = main_monitor_right_rect.bottomleft
    for i in range(NB_TRACKS):
        samples = np.max(engine.get_track_graph(i), axis=0)
        freq = get_freq(samples)
        tone = freq_to_tone(freq)

        draw_text(
            screen,
            f"{i + 1} {tone_to_str(tone)}",
            track_rect,
        )

        track_rect.top = track_rect.bottom
