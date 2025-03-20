from audio_node import AudioNode, an
import numpy as np
from config import SAMPLE_RATE, NB_TRACKS
from mixer import Mixer
from modulate import Modulate
from scheduler import Scheduler
from value import Value


class Engine(AudioNode):
    def __init__(self):
        mixer = an(Mixer(NB_TRACKS))
        self.__track_levels = []
        self.__track_schedulers = []
        for i in range(NB_TRACKS):
            level = an(Value(1.0))
            scheduler = an(Scheduler())
            mixer.set_track(i, an(Modulate(level, scheduler)))
            self.__track_levels.append(level)
            self.__track_schedulers.append(scheduler)
        self.__main_level = an(Value(1.0))
        output = an(Modulate(mixer, self.__main_level))
        self.__node = output

    def send(self, frames: int | None):
        if frames is None:
            return np.array([])
        samples = self.__node.send(frames)
        return samples

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def add_note(self, track: int, node: AudioNode, release: float, hold: float = 3600):
        self.__track_schedulers[track].add(node, release, hold)


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    ngin = Engine()
    next(ngin)
    frames = SAMPLE_RATE // 10
    parts = []
    for i in range(10):
        parts.append(ngin.send(frames))

    out = np.hstack(parts)
    t = np.arange(len(out)) / SAMPLE_RATE

    plt.plot(t, out)
    plt.show()
