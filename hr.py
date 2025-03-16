from audio_node import AudioNode, an
import numpy as np
from config import SAMPLE_RATE
from release import Release


class Hr(AudioNode):
    def __init__(self, release: float, hold: float = 3600):
        self.__release = an(Release(release))
        self.set_hold(hold)
        self.__elapsed_frames = 0

    def send(self, frames: int | None):
        if frames is None:
            return np.array([])
        parts = []

        if self.__elapsed_frames < self.__hold:
            hold_frames = min(frames, self.__hold - self.__elapsed_frames)
            parts.append(np.ones(hold_frames))
            frames -= hold_frames
            self.__elapsed_frames += hold_frames

        if frames > 0:
            parts.append(self.__release.send(frames))
            self.__elapsed_frames += frames
        return np.hstack(parts)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def off(self):
        self.__hold = self.__elapsed_frames

    def set_hold(self, hold: float):
        self.__hold = round(hold * SAMPLE_RATE)


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    val = an(Hr(0.5))
    val.set_hold(1)
    frames = SAMPLE_RATE // 10
    print(frames)
    parts = []
    for i in range(20):
        # if i == 9:
        #     val.off()
        parts.append(val.send(frames))

    out = np.hstack(parts)
    t = np.arange(len(out)) / SAMPLE_RATE

    plt.plot(t, out)
    plt.show()
