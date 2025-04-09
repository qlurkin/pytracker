from enum import Enum, auto


class Key(Enum):
    Up = auto()
    Down = auto()
    Right = auto()
    Left = auto()
    Edit = auto()
    Shift = auto()
    Option = auto()
    Play = auto()


class Event(Enum):
    MoveUp = auto()
    MoveDown = auto()
    MoveLeft = auto()
    MoveRight = auto()
    ShiftMoveUp = auto()
    ShiftMoveDown = auto()
    ShiftMoveLeft = auto()
    ShiftMoveRight = auto()
    EditUp = auto()
    EditDown = auto()
    EditLeft = auto()
    EditRight = auto()
    Edit = auto()
    Clear = auto()
    Play = auto()
    ShiftPlay = auto()
