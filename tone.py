from typing import Optional


SEMITONE_STR = ["C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#", "A-", "A#", "B-"]


class Tone:
    def __init__(self, semitone: int = 0, octave: int = 4):
        self.__semitone = semitone
        self.__octave = octave

    @property
    def semitone(self):
        return self.__semitone

    @property
    def octave(self):
        return self.__octave

    @property
    def frequency(self):
        base_frequency = 440
        semitone_ratio = 2 ** (1 / 12)
        semitone_diff = (self.__octave - 4) * 12 + self.__semitone - 9
        return base_frequency * semitone_ratio**semitone_diff

    def __str__(self):
        return f"{SEMITONE_STR[self.__semitone]}{self.__octave}"

    def up(self, n: int):
        semitone = self.semitone
        octave = self.octave

        for _ in range(n):
            if semitone == 11:
                octave += 1
            semitone = (semitone + 1) % 12

        self.__semitone = semitone
        self.__octave = octave

    def down(self, n: int):
        semitone = self.semitone
        octave = self.octave

        for _ in range(n):
            if semitone == 0:
                octave -= 1
            semitone = (semitone - 1) % 12

        self.__semitone = semitone
        self.__octave = octave


def tone_to_str(tone: Optional[Tone]):
    if tone is None:
        return "---"
    else:
        return str(tone)
