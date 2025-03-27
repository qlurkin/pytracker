import pygame
import numpy as np

from engine import Engine
from config import NB_TRACKS
from tone import tone_to_str
from util import freq_to_tone, get_freq
from views.font import GRID_HEIGHT, GRID_WIDTH, draw_text


def output_monitor(screen: pygame.Surface, rect: pygame.Rect, engine: Engine):
    for i in range(NB_TRACKS):
        samples = np.max(engine.get_track_graph(i), axis=0)
        freq = get_freq(samples)
        tone = freq_to_tone(freq)

        draw_text(
            screen,
            f"{i + 1} {tone_to_str(tone)}",
            pygame.Rect(
                rect.left, rect.top + i * (GRID_HEIGHT), 5 * GRID_WIDTH, GRID_HEIGHT
            ),
        )
