from dataclasses import dataclass
from typing import List
from alapo.app.Piece import PieceColorEnum, Piece, PieceTypeEnum
from alapo.app.config import Config


@dataclass
class BoardInput:
    x: int
    y: int


@dataclass
class Move:
    origin: BoardInput
    destination: BoardInput


class Board:
    def __init__(self) -> None:
        self.__matrix: List[List[Piece | None]] = [
            [None for _ in range(Config.BOARD_SIZE)] for _ in range(Config.BOARD_SIZE)
        ]

    def setup(self) -> None:
        self.__matrix[0] = [
            Piece(tipo=PieceTypeEnum.SQUARE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.SQUARE_SMALL, cor=PieceColorEnum.BLACK),
            None,
            None,
            Piece(tipo=PieceTypeEnum.SQUARE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.SQUARE_LARGE, cor=PieceColorEnum.WHITE),
        ]
        self.__matrix[1] = [
            Piece(tipo=PieceTypeEnum.TRIANGLE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.TRIANGLE_SMALL, cor=PieceColorEnum.BLACK),
            None,
            None,
            Piece(tipo=PieceTypeEnum.TRIANGLE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.TRIANGLE_LARGE, cor=PieceColorEnum.WHITE),
        ]
        self.__matrix[2] = [
            Piece(tipo=PieceTypeEnum.CIRCLE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.CIRCLE_SMALL, cor=PieceColorEnum.BLACK),
            None,
            None,
            Piece(tipo=PieceTypeEnum.CIRCLE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.CIRCLE_LARGE, cor=PieceColorEnum.WHITE),
        ]
        self.__matrix[3] = [
            Piece(tipo=PieceTypeEnum.CIRCLE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.CIRCLE_SMALL, cor=PieceColorEnum.BLACK),
            None,
            None,
            Piece(tipo=PieceTypeEnum.CIRCLE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.CIRCLE_LARGE, cor=PieceColorEnum.WHITE),
        ]
        self.__matrix[4] = [
            Piece(tipo=PieceTypeEnum.TRIANGLE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.TRIANGLE_SMALL, cor=PieceColorEnum.BLACK),
            None,
            None,
            Piece(tipo=PieceTypeEnum.TRIANGLE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.TRIANGLE_LARGE, cor=PieceColorEnum.WHITE),
        ]
        self.__matrix[5] = [
            Piece(tipo=PieceTypeEnum.SQUARE_LARGE, cor=PieceColorEnum.BLACK),
            Piece(tipo=PieceTypeEnum.SQUARE_SMALL, cor=PieceColorEnum.BLACK),
            None,
            None,
            Piece(tipo=PieceTypeEnum.SQUARE_SMALL, cor=PieceColorEnum.WHITE),
            Piece(tipo=PieceTypeEnum.SQUARE_LARGE, cor=PieceColorEnum.WHITE),
        ]

    def apply_move(self, origin: BoardInput, dest: BoardInput) -> None:
        i, j, k, l = origin.x, origin.y, dest.x, dest.y
        self.__matrix[k][l] = self.__matrix[i][j]
        self.__matrix[i][j] = None

    @property
    def matrix(self) -> List[List[Piece | None]]:
        return self.__matrix

    def read(self, coordinates: BoardInput) -> Piece | None:
        return self.__matrix[coordinates.x][coordinates.y]
