from time import perf_counter as time
from typing import Optional
from ads import Ads
from audio_node import AudioNode, an
from config import NB_TRACKS
from engine import Engine
from modulate import Modulate
from pan import Pan
from sine_oscilator import SineOscilator
from tone import Tone
from value import Value


class Instrument:
    def __init__(self, id: int):
        self.__id = id

    def make_note(self, frequency) -> AudioNode:
        return an(
            Modulate(
                an(
                    Pan(
                        an(SineOscilator(frequency)),
                        an(Value(0.5)),
                    )
                ),
                an(Ads(0.01, 0.1, 0.8)),
            )
        )

    def get_release(self) -> float:
        return 0.5

    def get_hold(self) -> float:
        return 0.5


class InstrumentInstance:
    def __init__(self, instrument: Instrument):
        # Table should probably be here
        self.__instrument = instrument

    def get(self) -> Instrument:
        return self.__instrument


class Step:
    def __init__(self, tone: Tone):
        self.__tone = tone
        self.__instrument: Optional[InstrumentInstance] = None

    def play(self, track: int, engine: Engine):
        if self.__instrument is None:
            return
        instrument = self.__instrument.get()
        node = instrument.make_note(self.__tone.frequency)
        release = instrument.get_release()
        hold = instrument.get_hold()
        engine.add_note(track, node, release, hold)


class Phrase:
    def __init__(self, id: int):
        self.__id = id
        self.__steps: list[Optional[Step]] = [None for _ in range(16)]

    def __getitem__(self, index: int):
        return self.__steps[index]

    def __len__(self):
        return len(self.__steps)


class PhraseInstance:
    def __init__(self, phrase: Phrase):
        self.__phrase: Phrase = phrase
        self.__cursor: int = 0

    def cursor_bump(self) -> bool:
        self.__cursor += 1
        res = False
        if self.__cursor == len(self.__phrase):
            self.__cursor = 0
            res = True
        return res

    def get_step(self) -> Optional[Step]:
        return self.__phrase[self.__cursor]


class Chain:
    def __init__(self, id: int):
        self.__id = id
        self.__phrases: list[Optional[PhraseInstance]] = [None for _ in range(16)]

    def __getitem__(self, index: int):
        return self.__phrases[index]

    def __len__(self):
        return len(self.__phrases)


class ChainInstance:
    def __init__(self, chain: Chain):
        self.__chain: Chain = chain
        self.__cursor: int = 0

    def cursor_bump(self) -> bool:
        phrase = self.__chain[self.__cursor]
        if phrase is None:
            return False
        if phrase.cursor_bump():
            self.__cursor += 1
            if (
                self.__cursor == len(self.__chain)
                or self.__chain[self.__cursor] is None
            ):
                self.__cursor = 0
            return True
        return False

    def get_step(self) -> Optional[Step]:
        phrase = self.__chain[self.__cursor]
        if phrase is not None:
            return phrase.get_step()
        return None


class Sequencer:
    def __init__(self, engine: Engine):
        self.__engine = engine
        self.__tempo: int = 128
        self.__last_tick_time: float = time()
        self.step_count = 0
        self.__groove: list[int] = [6]
        self.__groove_index: int = 0
        self.__remaining_ticks_before_next_step = self.__groove[self.__groove_index]
        self.__song: list[list[Optional[ChainInstance]]] = [
            [None for _ in range(256)] for _ in range(NB_TRACKS)
        ]
        self.__cursors: list[int] = [0 for _ in range(NB_TRACKS)]
        self.__chains: list[Optional[Chain]] = [None for _ in range(256)]
        self.__phrases: list[Optional[Phrase]] = [None for _ in range(256)]
        self.__instruments: list[Optional[Instrument]] = [None for _ in range(128)]

    def get_tempo(self):
        return self.__tempo

    def set_tempo(self, value: int):
        self.__tempo = value

    def tick_time(self):
        return 60 / (self.__tempo * 24)

    def get_step(self, track: int) -> Optional[Step]:
        chain = self.__song[track][self.__cursors[track]]
        if chain is not None:
            return chain.get_step()
        return None

    def cursor_bump(self, track: int):
        chain = self.__song[track][self.__cursors[track]]
        if chain is None:
            return
        if chain.cursor_bump():
            self.__cursors[track] += 1
            if (
                self.__cursors[track] == len(self.__song[track])
                or self.__song[track][self.__cursors[track]] is None
            ):
                # TODO: should rewind to the first non None chain
                self.__cursors[track] = 0

    def step(self):
        self.step_count += 1
        for i in range(NB_TRACKS):
            self.cursor_bump(i)
            step = self.get_step(i)
            if step is not None:
                step.play(i, self.__engine)

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
