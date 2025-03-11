import numpy as np
from zero import ZERO
from audio_node import AudioNode


class Mixer(AudioNode):
    def __init__(self, nb_tracks):
        self.__tracks = [ZERO] * nb_tracks
        self.__master_volume = 0.5

    def send(self, frames: int | None):
        if frames is None:
            return np.array([])
        samples = np.zeros(frames)
        for track in self.__tracks:
            samples += track.send(frames)
        samples *= self.__master_volume
        return samples

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def set_track(self, id: int, node: AudioNode | None):
        if node is None:
            node = ZERO
        self.__tracks[id] = node
