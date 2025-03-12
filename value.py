from audio_node import AudioNode
import numpy as np
from config import SAMPLE_RATE

CHANGE_RATE = 5  # gain per seconds


class Value(AudioNode):
    def __init__(self, value: float):
        self.__value = value
        self.__target = value

    def send(self, frames: int | None):
        if frames is None:
            return np.array([])
        parts = []
        if self.__value != self.__target:
            diff = self.__target - self.__value
            sign = np.sign(diff)
            ramp_frames = min(frames, round(SAMPLE_RATE * abs(diff) / CHANGE_RATE))
            samples = (
                np.arange(ramp_frames) * sign * CHANGE_RATE / SAMPLE_RATE + self.__value
            )
            parts.append(samples)
            self.__value = samples[-1]
            frames -= ramp_frames
        if frames > 0:
            samples = np.full(frames, self.__target)
            parts.append(samples)
            self.__value = self.__target
        return np.hstack(parts)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def set_value(self, value: float):
        self.__target = value


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    val = Value(0.1)
    next(val)
    frames = SAMPLE_RATE // 10
    print(frames)
    parts = []
    for i in range(10):
        if i == 2:
            val.set_value(0.9)
        if i == 5:
            val.set_value(0.2)
        if i == 6:
            val.set_value(1.0)
        parts.append(val.send(frames))

    out = np.hstack(parts)
    t = np.arange(len(out)) / SAMPLE_RATE

    plt.plot(t, out)
    plt.show()
