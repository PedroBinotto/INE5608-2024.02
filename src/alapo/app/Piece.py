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
    def __init__(self, tipo: PieceTypeEnum, cor: PieceColorEnum) -> None:
        self.__tipo = tipo
        self.__cor = cor

    @property
    def tipo(self) -> PieceTypeEnum:
        return self.__tipo

    @property
    def cor(self) -> PieceColorEnum:
        return self.__cor
