from typing import List
from alapo.app.Piece import PieceColorEnum, Piece, PieceTypeEnum
from alapo.app.config import Config


class Board:
    def __init__(self) -> None:
        self.__matrix: List[List[Piece | None]] = [
            [None for _ in range(Config.BOARD_SIZE)] for _ in range(Config.BOARD_SIZE)
        ]

    def setup(self) -> None:
        self.__matrix[5] = [
            Piece(tipo=PieceTypeEnum.SQUARE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.TRIANGLE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.CIRCLE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.CIRCLE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.TRIANGLE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.SQUARE_LARGE, cor=PieceColorEnum.BLACK),
        ]
        self.__matrix[4] = [
            Piece(tipo=PieceTypeEnum.SQUARE_SMALL, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.TRIANGLE_SMALL, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.CIRCLE_SMALL, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.CIRCLE_SMALL, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.TRIANGLE_SMALL, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.SQUARE_SMALL, cor=PieceColorEnum.BLACK),
        ]
        self.__matrix[1] = [
            Piece(tipo=PieceTypeEnum.SQUARE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.TRIANGLE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.CIRCLE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.CIRCLE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.TRIANGLE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.SQUARE_SMALL, cor=PieceColorEnum.WHITE),
        ]
        self.__matrix[0] = [
            Piece(tipo=PieceTypeEnum.SQUARE_LARGE, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.TRIANGLE_LARGE, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.CIRCLE_LARGE, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.CIRCLE_LARGE, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.TRIANGLE_LARGE, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.SQUARE_LARGE, cor=PieceColorEnum.WHITE),
        ]

    @property
    def matrix(self) -> List[List[Piece | None]]:
        return self.__matrix
