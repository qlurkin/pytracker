import numpy as np

from audio_node import AudioNode, an


def Zero() -> AudioNode:
    frames = yield np.array([])
    while True:
        frames = yield np.zeros(frames)


def ZeroStereo() -> AudioNode:
    frames = yield np.array([])
    while True:
        frames = yield np.zeros((2, frames))


ZERO = an(Zero())
ZERO_STEREO = an(ZeroStereo())
