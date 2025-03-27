import numpy as np
from zero import ZERO_STEREO
from audio_node import AudioNode


class Mixer(AudioNode):
    def __init__(self, nb_tracks):
        self.__tracks = [ZERO_STEREO] * nb_tracks

    def send(self, frames: int | None):
        if frames is None:
            return np.array([])
        samples = np.zeros((2, frames))
        for track in self.__tracks:
            samples += track.send(frames)
        # samples /= len(self.__tracks)
        return samples

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def set_track(self, id: int, node: AudioNode | None):
        if node is None:
            node = ZERO_STEREO
        self.__tracks[id] = node
