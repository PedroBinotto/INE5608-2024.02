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
        tmp = self.__matrix[i][j]
        self.__matrix[i][j] = None
        self.__matrix[k][l] = tmp

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
            target = checks[0]

            def ort_filter(coord: Coordinates) -> bool:
                candidates_one = [
                    PieceTypeEnum.SQUARE_SMALL,
                    PieceTypeEnum.CIRCLE_SMALL,
                ]
                candidates_n = [PieceTypeEnum.SQUARE_LARGE, PieceTypeEnum.CIRCLE_LARGE]
                pass

            def diag_filter(coord: Coordinates) -> bool:
                candidates_one = [
                    PieceTypeEnum.TRIANGLE_SMALL_SMALL,
                    PieceTypeEnum.CIRCLE_SMALL,
                ]
                candidates_n = [
                    PieceTypeEnum.TRIANGLE_SMALL_LARGE,
                    PieceTypeEnum.CIRCLE_LARGE,
                ]

            possible_captures = []

            orthogonals = filter(ort_filter, self.__trace_orthogonal(target))
            diagonals = filter(diag_filter, self.__trace_diagonal(target))
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
        x, y = origin.x, origin.y
        rows = Config.BOARD_SIZE
        cols = Config.BOARD_SIZE
        diagonals = []

        # Top-left diagonal
        i, j = x - 1, y - 1
        while i >= 0 and j >= 0:
            c = Coordinates(i, j)
            if self.read(c) is not None:
                break
            diagonals.append(c)
            if one_step:
                break
            i -= 1
            j -= 1

        # Top-right diagonal
        i, j = x - 1, y + 1
        while i >= 0 and j < cols:
            c = Coordinates(i, j)
            if self.read(c) is not None:
                break
            diagonals.append(c)
            if one_step:
                break
            i -= 1
            j += 1

        # Bottom-left diagonal
        i, j = x + 1, y - 1
        while i < rows and j >= 0:
            c = Coordinates(i, j)
            if self.read(c) is not None:
                break
            diagonals.append(c)
            if one_step:
                break
            i += 1
            j -= 1

        # Bottom-right diagonal
        i, j = x + 1, y + 1
        while i < rows and j < cols:
            c = Coordinates(i, j)
            if self.read(c) is not None:
                break
            diagonals.append(c)
            if one_step:
                break
            i += 1
            j += 1

        return diagonals

    def __trace_orthogonal(
        self, origin: Coordinates, one_step: bool = False
    ) -> list[Coordinates]:
        x, y = origin.x, origin.y
        rows = Config.BOARD_SIZE
        cols = Config.BOARD_SIZE
        orthogonals = []

        # Up
        i = x - 1
        while i >= 0:
            c = Coordinates(i, y)
            if self.read(c) is not None:
                break
            orthogonals.append(c)
            if one_step:
                break
            i -= 1

        # Down
        i = x + 1
        while i < rows:
            c = Coordinates(i, y)
            if self.read(c) is not None:
                break
            orthogonals.append(c)
            if one_step:
                break
            i += 1

        # Left
        j = y - 1
        while j >= 0:
            c = Coordinates(x, j)
            if self.read(c) is not None:
                break
            orthogonals.append(c)
            if one_step:
                break
            j -= 1

        # Right
        j = y + 1
        while j < cols:
            c = Coordinates(x, j)
            if self.read(c) is not None:
                break
            orthogonals.append(c)
            if one_step:
                break
            j += 1

        return orthogonals
