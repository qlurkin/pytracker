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
    tones = []
    for i in range(NB_TRACKS):
        samples = np.max(engine.get_track_graph(i), axis=0)
        freq = get_freq(samples)
        tone = freq_to_tone(freq)
        if tone is not None:
            tones.append(tone)

        draw_text(
            screen,
            f"{i + 1} {tone_to_str(tone)}",
            track_rect,
        )

        track_rect.top = track_rect.bottom

    piano_rect = pygame.Rect(0, 0, (rect.width // 7 + 1) * 7, GRID_HEIGHT)
    piano_rect.topright = (rect.right, track_rect.bottom)
    pygame.draw.lines(
        screen,
        (255, 255, 255),
        True,
        [
            piano_rect.topleft,
            piano_rect.topright,
            piano_rect.bottomright,
            piano_rect.bottomleft,
        ],
    )
    piano_key_width = piano_rect.width // 7
    for i in range(6):
        pos = piano_rect.left + (i + 1) * piano_key_width
        pygame.draw.line(
            screen, (255, 255, 255), (pos, piano_rect.top), (pos, piano_rect.bottom)
        )

    half_key = piano_key_width // 2

    semitones_pos = [
        half_key,
        piano_key_width,
        half_key + piano_key_width,
        2 * piano_key_width,
        half_key + 2 * piano_key_width,
        half_key + 3 * piano_key_width,
        4 * piano_key_width,
        half_key + 4 * piano_key_width,
        5 * piano_key_width,
        half_key + 5 * piano_key_width,
        6 * piano_key_width,
        half_key + 6 * piano_key_width,
    ]

    for i in [1, 3, 6, 8, 10]:
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            pygame.Rect(
                piano_rect.left + semitones_pos[i] - 2,
                piano_rect.top,
                5,
                piano_rect.height / 2,
            ),
        )

    for tone in tones:
        pygame.draw.circle(
            screen,
            (255, 0, 255),
            (piano_rect.left + semitones_pos[tone.semitone], piano_rect.centery),
            (piano_key_width - 2) / 2,
        )
