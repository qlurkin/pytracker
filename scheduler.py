from numpy.typing import NDArray
from audio_node import AudioNode, an
import numpy as np
from config import SAMPLE_RATE
from hr import Hr
from modulate import Modulate


class Scheduler(AudioNode):
    class Note:
        def __init__(self, node: AudioNode, release: float, hold: float):
            self.__hr = an(Hr(release, hold))
            self.__node = an(Modulate(self.__hr, node))

        def done(self) -> bool:
            return self.__hr.done()

        def off(self):
            self.__hr.off()

        def send(self, frames: int) -> NDArray[np.floating]:
            return self.__node.send(frames)

    def __init__(self):
        self.__notes = []
        pass

    def send(self, frames: int | None):
        if frames is None:
            return np.array([])
        samples = np.zeros((2, frames))
        for note in self.__notes:
            samples += note.send(frames)
        self.cleanup()
        samples /= 2
        return samples

    def cleanup(self):
        self.__notes = list(filter(lambda n: not n.done(), self.__notes))

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def add(self, node: AudioNode, release: float, hold: float = 3600):
        if len(self.__notes) > 0:
            self.__notes[-1].off()
        self.__notes.append(self.Note(node, release, hold))


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    sched = Scheduler()
    next(sched)
    frames = SAMPLE_RATE // 10
    print(frames)
    parts = []
    for i in range(10):
        parts.append(sched.send(frames))

    out = np.hstack(parts)
    t = np.arange(len(out)) / SAMPLE_RATE

    plt.plot(t, out)
    plt.show()
