from time import perf_counter as time
from typing import Optional
from config import NB_TRACKS
from tone import Tone


class Note:
    def __init__(self, tone: Tone):
        self.__tone = tone


class Phrase:
    def __init__(self, id: int):
        self.__id = id
        self.__notes: list[Optional[Note]] = [None for _ in range(16)]


class PhraseInstance:
    def __init__(self, phrase: Phrase):
        self.__phrase: Phrase = phrase
        self.__cursor: int = 0


class Chain:
    def __init__(self, id: int):
        self.__id = id
        self.__phrases: list[Optional[PhraseInstance]] = [None for _ in range(16)]


class ChainInstance:
    def __init__(self, chain: Chain):
        self.__chain: Chain = chain
        self.__cursor: int = 0


class Sequencer:
    def __init__(self):
        self.__tempo: int = 128
        self.__last_tick_time: float = time()
        self.step_count = 0
        self.__groove: list[int] = [6]
        self.__groove_index: int = 0
        self.__remaining_ticks_before_next_step = self.__groove[self.__groove_index]
        self.__song: list[list[Optional[ChainInstance]]] = [
            [None for _ in range(16)] for _ in range(NB_TRACKS)
        ]
        self.__cursors: list[int] = [0 for _ in range(NB_TRACKS)]
        self.__chains: list[Optional[Chain]] = [None for _ in range(128)]
        self.__phrases: list[Optional[Phrase]] = [None for _ in range(128)]

    def get_tempo(self):
        return self.__tempo

    def set_tempo(self, value: int):
        self.__tempo = value

    def tick_time(self):
        return 60 / (self.__tempo * 24)

    def step(self):
        self.step_count += 1

    def tick(self):
        self.__remaining_ticks_before_next_step -= 1
        if self.__remaining_ticks_before_next_step == 0:
            self.step()
            self.__groove_index = (self.__groove_index + 1) % len(self.__groove)
            self.__remaining_ticks_before_next_step = self.__groove[self.__groove_index]

    def update(self):
        tick_time = self.tick_time()
        if time() - self.__last_tick_time >= tick_time:
            self.__last_tick_time += tick_time
            self.tick()
