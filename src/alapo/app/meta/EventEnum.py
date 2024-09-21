from enum import Enum, auto


class EventEnum(Enum):
    START_APP = auto()
    RECEIVE_START_MATCH = auto()
    RECEIVE_MOVE = auto()
    RECEIVE_WITHDRAWAL = auto()
