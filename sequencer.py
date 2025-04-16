from __future__ import annotations
from time import perf_counter as time
from typing import Optional, Protocol
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
    def __init__(self):
        pass

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
    def __init__(self, id: int):
        # Table should probably be here
        self.__id = id

    @property
    def id(self) -> int:
        return self.__id


class Step:
    def __init__(self, tone: Tone):
        self.__tone = tone
        self.__instrument: Optional[InstrumentInstance] = None

    # def play(self, track: int, engine: Engine):
    #     if self.__instrument is None:
    #         return
    #     instrument = self.__instrument.instrument
    #     node = instrument.make_note(self.__tone.frequency)
    #     release = instrument.get_release()
    #     hold = instrument.get_hold()
    #     engine.add_note(track, node, release, hold)

    def set_instrument(self, id: Optional[int]):
        if id is None:
            self.__instrument = None
            return
        self.__instrument = InstrumentInstance(id)

    def get_instrument(self) -> Optional[int]:
        if self.__instrument is None:
            return None
        return self.__instrument.id

    def get_tone(self) -> Tone:
        return self.__tone

    def set_tone(self, tone: Tone):
        self.__tone = tone


class Phrase:
    def __init__(self):
        self.__steps: list[Optional[Step]] = [None for _ in range(16)]

    def __getitem__(self, index: int) -> Optional[Step]:
        return self.__steps[index]

    def __setitem__(self, index: int, step: Optional[Step]):
        self.__steps[index] = step

    def __len__(self) -> int:
        return len(self.__steps)


class PhraseInstance:
    def __init__(self, id: int):
        self.__id = id

    @property
    def id(self):
        return self.__id

    # def cursor_bump(self, max: int) -> bool:
    #     self.__cursor += 1
    #     res = False
    #     if self.__cursor == max:
    #         self.__cursor = 0
    #         res = True
    #     return res

    # def get_step(self) -> Optional[Step]:
    #     return self.__phrase[self.__cursor]


class Chain:
    def __init__(self):
        self.__phrases: list[Optional[PhraseInstance]] = [None for _ in range(16)]

    def __getitem__(self, index: int) -> Optional[int]:
        instance = self.__phrases[index]
        if instance is None:
            return None
        return instance.id

    def get_instance(self, index: int) -> Optional[PhraseInstance]:
        return self.__phrases[index]

    def __setitem__(self, index: int, phrase_id: Optional[int]):
        if phrase_id is None:
            self.__phrases[index] = None
            return
        self.__phrases[index] = PhraseInstance(phrase_id)

    def __len__(self):
        return len(self.__phrases)


class ChainInstance:
    def __init__(self, id: int):
        self.__id = id

    @property
    def id(self):
        return self.__id

    # def cursor_bump(self) -> bool:
    #     instance = self.__chain.get_instance(self.__cursor)
    #     if instance is None:
    #         return False
    #     if instance.cursor_bump():
    #         self.__cursor += 1
    #         if (
    #             self.__cursor == len(self.__chain)
    #             or self.__chain.get_instance(self.__cursor) is None
    #         ):
    #             self.__cursor = 0
    #         return True
    #     return False
    #
    # def get_step(self) -> Optional[Step]:
    #     instance = self.__chain.get_instance(self.__cursor)
    #     if instance is not None:
    #         return instance.get_step()
    #     return None


class Track:
    def __init__(self):
        self.__chains: list[Optional[ChainInstance]] = [None for _ in range(256)]

    # def cursor_bump(self) -> bool:
    #     instance = self.__chains[self.__cursor]
    #     if instance is None:
    #         return False
    #     if instance.cursor_bump():
    #         self.__cursor += 1
    #         if (
    #             self.__cursor == len(self.__chains)
    #             or self.__chains[self.__cursor] is None
    #         ):
    #             # TODO: should rewind to the first non None chain
    #             self.__cursor = 0
    #             return True
    #     return False
    #
    # def get_step(self) -> Optional[Step]:
    #     chain = self.__chains[self.__cursor]
    #     if chain is not None:
    #         return chain.get_step()
    #     return None

    def __getitem__(self, index: int) -> Optional[int]:
        instance = self.__chains[index]
        if instance is None:
            return None
        return instance.id

    def __setitem__(self, index: int, chain_id: Optional[int]):
        if chain_id is None:
            self.__chains[index] = None
            return
        self.__chains[index] = ChainInstance(chain_id)

    def __len__(self):
        return len(self.__chains)


class Player(Protocol):
    def step(self, sequencer: Sequencer) -> Optional[Step]: ...


class PhrasePlayer:
    def __init__(self, phrase_id: int):
        self.__id = phrase_id
        self.__cursor = 0

    def step(self, sequencer: Sequencer):
        self.__cursor = (self.__cursor + 1) % 16
        phrase = sequencer.phrase[self.__id]
        if phrase is None:
            return
        step = phrase[self.__cursor]
        sequencer.play(0, step)


class Sequencer:
    def __init__(self, engine: Engine):
        self.__engine = engine
        self.__tempo: int = 128
        self.__last_tick_time: float = time()
        self.step_count = 0
        self.__groove: list[int] = [6]
        self.__groove_index: int = 0
        self.__remaining_ticks_before_next_step = self.__groove[self.__groove_index]
        self.__tracks: list[Track] = [Track() for _ in range(NB_TRACKS)]
        self.__chains: list[Optional[Chain]] = [None for _ in range(256)]
        self.__phrases: list[Optional[Phrase]] = [None for _ in range(256)]
        self.__instruments: list[Optional[Instrument]] = [None for _ in range(256)]
        self.__player: Player = PhrasePlayer(0)

        ##### TEST #####
        self.__instruments[0] = Instrument()
        step = Step(Tone())
        step.set_instrument(0)
        self.phrase[0] = Phrase()
        self.phrase[0][0] = step
        chain = Chain()
        chain[0] = 0
        self.chain[0] = chain

    @property
    def track(self):
        return self.__tracks

    @property
    def chain(self):
        return self.__chains

    @property
    def phrase(self):
        return self.__phrases

    @property
    def instrument(self):
        return self.__instruments

    def get_tempo(self):
        return self.__tempo

    def set_tempo(self, value: int):
        self.__tempo = value

    def tick_time(self):
        return 60 / (self.__tempo * 24)

    # def get_step(self, track: int) -> Optional[Step]:
    #     return self.__player.step(self)
    #
    # def cursor_bump(self, track: int):
    #     return self.__player.bump(self)

    def step(self):
        self.step_count += 1
        # for i in range(NB_TRACKS):
        #     self.cursor_bump(i)
        #     step = self.get_step(i)
        #     if step is not None:
        #         step.play(i, self.__engine)
        self.__player.step(self)

    def play(self, track: int, step: Optional[Step]):
        if step is None:
            return
        inst_id = step.get_instrument()
        if inst_id is None:
            return
        instrument = self.instrument[inst_id]
        if instrument is None:
            return
        node = instrument.make_note(step.get_tone().frequency)
        release = instrument.get_release()
        hold = instrument.get_hold()
        self.__engine.add_note(track, node, release, hold)

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
