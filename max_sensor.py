from audio_node import AudioNode
import numpy as np


class MaxSensor(AudioNode):
    def __init__(self, node: AudioNode):
        self.__value = np.float64(0.0)
        self.__node = node

    def send(self, frames: int | None):
        if frames is None:
            return np.array([])
        samples = self.__node.send(frames)
        self.__value = np.max(samples)
        return samples

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def get_value(self) -> float:
        return float(self.__value)
