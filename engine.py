from numpy.typing import NDArray
from audio_node import AudioNode, an
import numpy as np
from config import SAMPLE_RATE, NB_TRACKS
from graph_sensor import GraphSensor
from max_sensor import MaxSensor
from mixer import Mixer
from modulate import Modulate
from scheduler import Scheduler
from value import Value


GRAPH_SIZE = 2048


class Engine(AudioNode):
    def __init__(self):
        mixer = an(Mixer(NB_TRACKS))
        self.__track_levels = []
        self.__track_schedulers = []
        self.__track_sensors = []
        self.__track_graph_sensors = []
        for i in range(NB_TRACKS):
            level = an(Value(1.0))
            scheduler = an(Scheduler())
            track = an(Modulate(level, scheduler))
            max_sensor = an(MaxSensor(track))
            graph_sensor = an(GraphSensor(max_sensor, GRAPH_SIZE))
            mixer.set_track(i, graph_sensor)
            self.__track_levels.append(level)
            self.__track_schedulers.append(scheduler)
            self.__track_sensors.append(max_sensor)
            self.__track_graph_sensors.append(graph_sensor)
        self.__main_level = an(Value(1.0))
        output = an(Modulate(mixer, self.__main_level))
        self.__main_graph_sensor = an(GraphSensor(output, GRAPH_SIZE))
        self.__node = an(MaxSensor(self.__main_graph_sensor))

    def send(self, frames: int | None):
        if frames is None:
            return np.array([])
        samples = self.__node.send(frames)
        return samples

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def add_note(self, track: int, node: AudioNode, release: float, hold: float = 3600):
        self.__track_schedulers[track].add(node, release, hold)

    def get_output_sensor(self) -> list[float]:
        return self.__node.get_value()

    def get_track_sensor(self, track: int) -> float:
        return self.__track_sensors[track].get_value()

    def get_track_level(self, track: int) -> float:
        return self.__track_levels[track].get_value()

    def set_track_level(self, track: int, value: float):
        self.__track_levels[track].set_value(value)

    def get_main_level(self) -> float:
        return self.__main_level.get_value()

    def set_main_level(self, value: float):
        self.__main_level.set_value(value)

    def get_main_graph(self) -> NDArray:
        return self.__main_graph_sensor.get_values()

    def get_track_graph(self, track: int) -> NDArray:
        return self.__track_graph_sensors[track].get_values()


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
