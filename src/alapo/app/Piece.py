from enum import Enum, auto


class PieceTypeEnum(Enum):
    TRIANGLE_LARGE = auto()
    SQUARE_LARGE = auto()
    CIRCLE_LARGE = auto()
    TRIANGLE_SMALL = auto()
    SQUARE_SMALL = auto()
    CIRCLE_SMALL = auto()


class PieceColorEnum(Enum):
    BLACK = auto()
    WHITE = auto()


class Piece:
    def __init__(self, type: PieceTypeEnum, color: PieceColorEnum) -> None:
        self.__type = type
        self.__color = color

    @property
    def type(self) -> PieceTypeEnum:
        return self.__type

    @property
    def color(self) -> PieceColorEnum:
        return self.__color
