from tone import Tone
from copy import copy


class __ClipboardClass:
    def __init__(self):
        self.__tone = Tone()

    @property
    def tone(self):
        return copy(self.__tone)

    @tone.setter
    def tone(self, value):
        self.__tone = value


ClipBoard = __ClipboardClass()
