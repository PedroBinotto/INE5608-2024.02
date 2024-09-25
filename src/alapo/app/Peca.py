from alapo.app.TipoPecaEnum import TipoPecaEnum


class Peca:
    def __init__(self, tipo: TipoPecaEnum) -> None:
        self.__tipo = tipo

    @property
    def tipo(self) -> TipoPecaEnum:
        return self.__tipo
