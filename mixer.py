import numpy as np
from zero import zero
from audio_node import AudioNode

NB_TRACKS = 8

ZERO = zero()
next(ZERO)

__tracks = [ZERO] * NB_TRACKS
__master_volume = 0.5


def mixer() -> AudioNode:
    frames = yield np.array([])

    while True:
        samples = np.zeros(frames)
        for track in __tracks:
            samples += track.send(frames)
        samples *= __master_volume
        frames = yield samples


def set_track(id: int, node: AudioNode):
    __tracks[id] = node
