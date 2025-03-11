import numpy as np

from audio_node import AudioNode


def Zero() -> AudioNode:
    frames = yield np.array([])
    while True:
        frames = yield np.zeros(frames)
