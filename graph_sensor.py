from audio_node import AudioNode
import numpy as np


class GraphSensor(AudioNode):
    def __init__(self, node: AudioNode, size: int):
        self.__values = np.zeros(size)
        self.__size = size
        self.__node = node

    def send(self, frames: int | None):
        if frames is None:
            return np.array([])

        samples = self.__node.send(frames)
        if frames > self.__size:
            self.__values = samples[-self.__size :]
        else:
            self.__values = np.hstack([self.__values[frames - self.__size :], samples])
        return samples

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def get_values(self) -> float:
        return float(self.__values)
