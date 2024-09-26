from enum import Enum, auto


class TipoPecaEnum(Enum):
    TRIANGULAR_GRANDE = auto()
    QUADRADA_GRANDE = auto()
    CIRCULAR_GRANDE = auto()
    TRIANGULAR_PEQUENA = auto()
    QUADRADA_PEQUENA = auto()
    CIRCULAR_PEQUENA = auto()


class CorPecaEnum(Enum):
    PRETO = auto()
    BRANCO = auto()


class Peca:
    def __init__(self, tipo: TipoPecaEnum, cor: CorPecaEnum) -> None:
        self.__tipo = tipo
        self.__cor = cor

    @property
    def tipo(self) -> TipoPecaEnum:
        return self.__tipo

    @property
    def cor(self) -> CorPecaEnum:
        return self.__cor
