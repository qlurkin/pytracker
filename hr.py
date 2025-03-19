from audio_node import AudioNode, an
import numpy as np
from config import SAMPLE_RATE
from release import Release


class Hr(AudioNode):
    def __init__(self, release: float, hold: float = 3600):
        self.__release = an(Release(release))
        self.set_hold(hold)
        self.__elapsed_frames = 0
        self.__done = False
        self.__releasing = False

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
            self.__releasing = True
            release_samples = self.__release.send(frames)
            if release_samples[-1] == 0:
                self.__done = True
            parts.append(release_samples)
            self.__elapsed_frames += frames
        return np.hstack(parts)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def off(self):
        if not self.__releasing:
            self.__hold = self.__elapsed_frames

    def set_hold(self, hold: float):
        self.__hold = round(hold * SAMPLE_RATE)

    def done(self) -> bool:
        return self.__done


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    hr = an(Hr(0.5))
    hr.set_hold(1)
    frames = SAMPLE_RATE // 10
    print(frames)
    parts = []
    print(hr.done())
    for i in range(20):
        # if i == 9:
        #     val.off()
        parts.append(hr.send(frames))

    print(hr.done())

    out = np.hstack(parts)
    t = np.arange(len(out)) / SAMPLE_RATE

    plt.plot(t, out)
    plt.show()
