from typing import List
from alapo.app.Peca import Peca
from alapo.app.TipoPecaEnum import TipoPecaEnum
from alapo.app.config import Config


class Tabuleiro:
    def __init__(self) -> None:
        self.__matrix: List[List[Peca | None]] = [
            [None for _ in range(Config.BOARD_SIZE)] for _ in range(Config.BOARD_SIZE)]
        print(self.__matrix)

    def setup(self) -> None:
        self.__matrix[5] = [
            Peca(
                tipo=TipoPecaEnum.QUADRADA_GRANDE), Peca(
                tipo=TipoPecaEnum.TRIANGULAR_GRANDE), Peca(
                tipo=TipoPecaEnum.CIRCULAR_GRANDE), Peca(
                    tipo=TipoPecaEnum.CIRCULAR_GRANDE), Peca(
                        tipo=TipoPecaEnum.TRIANGULAR_GRANDE), Peca(
                            tipo=TipoPecaEnum.QUADRADA_GRANDE)]
        self.__matrix[4] = [
            Peca(
                tipo=TipoPecaEnum.QUADRADA_PEQUENA), Peca(
                tipo=TipoPecaEnum.TRIANGULAR_PEQUENA), Peca(
                tipo=TipoPecaEnum.CIRCULAR_PEQUENA), Peca(
                    tipo=TipoPecaEnum.CIRCULAR_PEQUENA), Peca(
                        tipo=TipoPecaEnum.TRIANGULAR_PEQUENA), Peca(
                            tipo=TipoPecaEnum.QUADRADA_PEQUENA)]
        self.__matrix[1] = [
            Peca(
                tipo=TipoPecaEnum.QUADRADA_PEQUENA), Peca(
                tipo=TipoPecaEnum.TRIANGULAR_PEQUENA), Peca(
                tipo=TipoPecaEnum.CIRCULAR_PEQUENA), Peca(
                    tipo=TipoPecaEnum.CIRCULAR_PEQUENA), Peca(
                        tipo=TipoPecaEnum.TRIANGULAR_PEQUENA), Peca(
                            tipo=TipoPecaEnum.QUADRADA_PEQUENA)]
        self.__matrix[0] = [
            Peca(
                tipo=TipoPecaEnum.QUADRADA_GRANDE), Peca(
                tipo=TipoPecaEnum.TRIANGULAR_GRANDE), Peca(
                tipo=TipoPecaEnum.CIRCULAR_GRANDE), Peca(
                    tipo=TipoPecaEnum.CIRCULAR_GRANDE), Peca(
                        tipo=TipoPecaEnum.TRIANGULAR_GRANDE), Peca(
                            tipo=TipoPecaEnum.QUADRADA_GRANDE)]

    @property
    def matrix(self) -> List[List[Peca | None]]:
        return self.__matrix
