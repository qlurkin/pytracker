import numpy as np

from audio_node import AudioNode, an


def Zero() -> AudioNode:
    frames = yield np.array([])
    while True:
        frames = yield np.zeros(frames)


ZERO = an(Zero)
