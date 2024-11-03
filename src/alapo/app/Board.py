from collections.abc import Callable
from dataclasses import dataclass
from typing import List
from alapo.app.Piece import PieceColorEnum, Piece, PieceTypeEnum
from alapo.app.config import Config


@dataclass
class Coordinates:
    x: int
    y: int


@dataclass
class Move:
    origin: Coordinates
    destination: Coordinates


class Board:
    def __init__(self) -> None:
        self.__matrix: List[List[Piece | None]] = [
            [None for _ in range(Config.BOARD_SIZE)] for _ in range(Config.BOARD_SIZE)
        ]

    def setup(self) -> None:
        self.__matrix[0] = [
            Piece(type=PieceTypeEnum.SQUARE_LARGE, color=PieceColorEnum.BLACK),
            Piece(type=PieceTypeEnum.SQUARE_SMALL, color=PieceColorEnum.BLACK),
            None,
            None,
            Piece(type=PieceTypeEnum.SQUARE_SMALL, color=PieceColorEnum.WHITE),
            Piece(type=PieceTypeEnum.SQUARE_LARGE, color=PieceColorEnum.WHITE),
        ]
        self.__matrix[1] = [
            Piece(type=PieceTypeEnum.TRIANGLE_LARGE, color=PieceColorEnum.BLACK),
            Piece(type=PieceTypeEnum.TRIANGLE_SMALL, color=PieceColorEnum.BLACK),
            None,
            None,
            Piece(type=PieceTypeEnum.TRIANGLE_SMALL, color=PieceColorEnum.WHITE),
            Piece(type=PieceTypeEnum.TRIANGLE_LARGE, color=PieceColorEnum.WHITE),
        ]
        self.__matrix[2] = [
            Piece(type=PieceTypeEnum.CIRCLE_LARGE, color=PieceColorEnum.BLACK),
            Piece(type=PieceTypeEnum.CIRCLE_SMALL, color=PieceColorEnum.BLACK),
            None,
            None,
            Piece(type=PieceTypeEnum.CIRCLE_SMALL, color=PieceColorEnum.WHITE),
            Piece(type=PieceTypeEnum.CIRCLE_LARGE, color=PieceColorEnum.WHITE),
        ]
        self.__matrix[3] = [
            Piece(type=PieceTypeEnum.CIRCLE_LARGE, color=PieceColorEnum.BLACK),
            Piece(type=PieceTypeEnum.CIRCLE_SMALL, color=PieceColorEnum.BLACK),
            None,
            None,
            Piece(type=PieceTypeEnum.CIRCLE_SMALL, color=PieceColorEnum.WHITE),
            Piece(type=PieceTypeEnum.CIRCLE_LARGE, color=PieceColorEnum.WHITE),
        ]
        self.__matrix[4] = [
            Piece(type=PieceTypeEnum.TRIANGLE_LARGE, color=PieceColorEnum.BLACK),
            Piece(type=PieceTypeEnum.TRIANGLE_SMALL, color=PieceColorEnum.BLACK),
            None,
            None,
            Piece(type=PieceTypeEnum.TRIANGLE_SMALL, color=PieceColorEnum.WHITE),
            Piece(type=PieceTypeEnum.TRIANGLE_LARGE, color=PieceColorEnum.WHITE),
        ]
        self.__matrix[5] = [
            Piece(type=PieceTypeEnum.SQUARE_LARGE, color=PieceColorEnum.BLACK),
            Piece(type=PieceTypeEnum.SQUARE_SMALL, color=PieceColorEnum.BLACK),
            None,
            None,
            Piece(type=PieceTypeEnum.SQUARE_SMALL, color=PieceColorEnum.WHITE),
            Piece(type=PieceTypeEnum.SQUARE_LARGE, color=PieceColorEnum.WHITE),
        ]

    def apply_move(self, move: Move) -> None:
        print("__apply_move", move)
        origin, destination = move.origin, move.destination
        i, j, k, l = origin.x, origin.y, destination.x, destination.y
        self.__matrix[k][l] = self.__matrix[i][j]
        self.__matrix[i][j] = None

    def get_available_pieces(self, color: PieceColorEnum) -> list[Coordinates]:
        line_n = 0 if color == PieceColorEnum.BLACK else Config.BOARD_SIZE - 1
        opp_color = (
            PieceColorEnum.WHITE
            if color == PieceColorEnum.BLACK
            else PieceColorEnum.BLACK
        )

        checks = []
        pieces = []

        for i in range(len(self.__matrix)):
            col = self.__matrix[i]
            if col[line_n] is not None and col[line_n].color == opp_color:
                checks.append(Coordinates(i, line_n))
            for j in range(len(col)):
                if col[j] is not None and col[j].color == color:
                    pieces.append(Coordinates(i, j))

        if len(checks) > 1:
            return []
        elif len(checks) == 1:

            def ort_filter(coord: Coordinates) -> bool:
                candidates_one = [
                    PieceTypeEnum.SQUARE_SMALL,
                    PieceTypeEnum.CIRCLE_SMALL,
                ]
                candidates_n = [PieceTypeEnum.SQUARE_LARGE, PieceTypeEnum.CIRCLE_LARGE]
                pass

            def diag_filter_filter(coord: Coordinates) -> bool:
                candidates_one = [
                    PieceTypeEnum.TRIANGLE_SMALL_SMALL,
                    PieceTypeEnum.CIRCLE_SMALL,
                ]
                candidates_n = [
                    PieceTypeEnum.TRIANGLE_SMALL_LARGE,
                    PieceTypeEnum.CIRCLE_LARGE,
                ]

            target = checks[0]
            possible_captures = []

            orthogonals = filter(ort_filter, self.__trace_orthogonal(target))
        else:
            return pieces

    def get_available_destinations(self, origin: Coordinates) -> list[Coordinates]:
        type = self.read(origin).type
        match type:
            case PieceTypeEnum.TRIANGLE_LARGE:
                return self.__trace_diagonal(origin)
            case PieceTypeEnum.TRIANGLE_SMALL:
                return self.__trace_diagonal(origin, one_step=True)
            case PieceTypeEnum.SQUARE_LARGE:
                return self.__trace_orthogonal(origin)
            case PieceTypeEnum.SQUARE_SMALL:
                return self.__trace_orthogonal(origin, one_step=True)
            case PieceTypeEnum.CIRCLE_LARGE:
                return self.__trace_diagonal(origin) + self.__trace_orthogonal(origin)
            case PieceTypeEnum.CIRCLE_SMALL:
                return self.__trace_diagonal(
                    origin, one_step=True
                ) + self.__trace_orthogonal(origin, one_step=True)

    @property
    def matrix(self) -> List[List[Piece | None]]:
        return self.__matrix

    def read(self, coordinates: Coordinates) -> Piece | None:
        return self.__matrix[coordinates.x][coordinates.y]

    def __trace_diagonal(
        self, origin: Coordinates, one_step: bool = False
    ) -> list[Coordinates]:
        diagonals: list[Coordinates] = []

        x, y = origin.x, origin.y

        transformers: list[tuple[Callable[[int], int], Callable[[int], int]]] = [
            (lambda x: x - 1, lambda y: y - y),
            (lambda x: x - 1, lambda y: y + y),
            (lambda x: x + 1, lambda y: y - y),
            (lambda x: x + 1, lambda y: y + y),
        ]

        limits: tuple[Callable[[int, int], bool]] = (
            lambda c, d: c >= 0 and d >= 0,
            lambda c, d: c >= 0 and d < Config.BOARD_SIZE,
            lambda c, d: c < Config.BOARD_SIZE and d >= 0,
            lambda c, d: c < Config.BOARD_SIZE and d < Config.BOARD_SIZE,
        )

        for idx, (tx, ty) in enumerate(transformers):
            i, j = tx(x), ty(y)

            while limits[idx](i, j):
                coord = Coordinates(i, j)
                print(coord)
                if self.read(coord) is not None:
                    break
                diagonals.append(coord)
                if one_step:
                    break
                i = tx(i)
                j = ty(j)

        print("diagonals", diagonals)
        return diagonals

    def __trace_orthogonal(
        self, origin: Coordinates, one_step: bool = False
    ) -> list[Coordinates]:
        orthogonals: List[Coordinates] = []
        x, y = origin.x, origin.y

        transformers: list[tuple[Callable[[int], int], Callable[[int], int]]] = [
            (lambda x: x - 1, lambda y: y),
            (lambda x: x + 1, lambda y: y),
            (lambda x: x, lambda y: y - 1),
            (lambda x: x, lambda y: y + 1),
        ]

        limits: list[Callable[[int, int], bool]] = [
            lambda c: c >= 0,
            lambda c: c < Config.BOARD_SIZE,
        ]

        for idx, (tx, ty) in enumerate(transformers):
            i, j = tx(x), ty(y)

            l_idx = idx % 2
            k = (i, j)[int(2 <= idx < 4)]

            while limits[l_idx](k):
                coord = Coordinates(i, j)
                print(coord)
                if self.read(coord) is not None:
                    break
                orthogonals.append(coord)
                if one_step:
                    break
                i = tx(i)
                j = ty(j)

        print("orthogonals", orthogonals)
        return orthogonals
