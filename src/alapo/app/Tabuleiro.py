from typing import List
from alapo.app.Peca import CorPecaEnum, Peca, TipoPecaEnum
from alapo.app.config import Config


class Tabuleiro:
    def __init__(self) -> None:
        self.__matrix: List[List[Peca | None]] = [
            [None for _ in range(Config.BOARD_SIZE)] for _ in range(Config.BOARD_SIZE)]
        print(self.__matrix)

    def setup(self) -> None:
        self.__matrix[5] = [
            Peca(
                tipo=TipoPecaEnum.QUADRADA_GRANDE, cor=CorPecaEnum.PRETO), Peca(
                tipo=TipoPecaEnum.TRIANGULAR_GRANDE, cor=CorPecaEnum.PRETO), Peca(
                tipo=TipoPecaEnum.CIRCULAR_GRANDE, cor=CorPecaEnum.PRETO), Peca(
                    tipo=TipoPecaEnum.CIRCULAR_GRANDE, cor=CorPecaEnum.PRETO), Peca(
                        tipo=TipoPecaEnum.TRIANGULAR_GRANDE, cor=CorPecaEnum.PRETO), Peca(
                            tipo=TipoPecaEnum.QUADRADA_GRANDE, cor=CorPecaEnum.PRETO)]
        self.__matrix[4] = [
            Peca(
                tipo=TipoPecaEnum.QUADRADA_PEQUENA, cor=CorPecaEnum.PRETO), Peca(
                tipo=TipoPecaEnum.TRIANGULAR_PEQUENA, cor=CorPecaEnum.PRETO), Peca(
                tipo=TipoPecaEnum.CIRCULAR_PEQUENA, cor=CorPecaEnum.PRETO), Peca(
                    tipo=TipoPecaEnum.CIRCULAR_PEQUENA, cor=CorPecaEnum.PRETO), Peca(
                        tipo=TipoPecaEnum.TRIANGULAR_PEQUENA, cor=CorPecaEnum.PRETO), Peca(
                            tipo=TipoPecaEnum.QUADRADA_PEQUENA, cor=CorPecaEnum.PRETO)]
        self.__matrix[1] = [
            Peca(
                tipo=TipoPecaEnum.QUADRADA_PEQUENA, cor=CorPecaEnum.BRANCO), Peca(
                tipo=TipoPecaEnum.TRIANGULAR_PEQUENA, cor=CorPecaEnum.BRANCO), Peca(
                tipo=TipoPecaEnum.CIRCULAR_PEQUENA, cor=CorPecaEnum.BRANCO), Peca(
                    tipo=TipoPecaEnum.CIRCULAR_PEQUENA, cor=CorPecaEnum.BRANCO), Peca(
                        tipo=TipoPecaEnum.TRIANGULAR_PEQUENA, cor=CorPecaEnum.BRANCO), Peca(
                            tipo=TipoPecaEnum.QUADRADA_PEQUENA, cor=CorPecaEnum.BRANCO)]
        self.__matrix[0] = [
            Peca(
                tipo=TipoPecaEnum.QUADRADA_GRANDE, cor=CorPecaEnum.BRANCO), Peca(
                tipo=TipoPecaEnum.TRIANGULAR_GRANDE, cor=CorPecaEnum.BRANCO), Peca(
                tipo=TipoPecaEnum.CIRCULAR_GRANDE, cor=CorPecaEnum.BRANCO), Peca(
                    tipo=TipoPecaEnum.CIRCULAR_GRANDE, cor=CorPecaEnum.BRANCO), Peca(
                        tipo=TipoPecaEnum.TRIANGULAR_GRANDE, cor=CorPecaEnum.BRANCO), Peca(
                            tipo=TipoPecaEnum.QUADRADA_GRANDE, cor=CorPecaEnum.BRANCO)]

    @property
    def matrix(self) -> List[List[Peca | None]]:
        return self.__matrix
