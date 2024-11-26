from dataclasses import dataclass
from typing import Callable, List
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
        origin, destination = move.origin, move.destination
        i, j, k, l = origin.x, origin.y, destination.x, destination.y
        tmp = self.__matrix[i][j]
        self.__matrix[i][j] = None
        self.__matrix[k][l] = tmp

    def get_available_pieces(self, color: PieceColorEnum) -> list[Coordinates]:
        pieces = []
        for i in range(len(self.__matrix)):
            col = self.__matrix[i]
            for j in range(len(col)):
                position = Coordinates(i, j)
                if (
                    col[j] is not None
                    and col[j].color == color
                    and len(self.get_available_destinations(position, color))
                ):
                    pieces.append(position)

        checks = self.__get_checks(color)

        match len(checks):
            case 0:
                return pieces
            case 1:
                return self.__get_contestants(checks.pop())
            case _:
                return []

    def get_available_destinations(
        self, origin: Coordinates, local_player_color: PieceColorEnum
    ) -> list[Coordinates]:
        checks = self.__get_checks(local_player_color)
        if checks:
            return checks

        type = self.read(origin).type
        match type:
            case PieceTypeEnum.TRIANGLE_LARGE:
                return self.__trace_diagonal(origin, local_player_color)

            case PieceTypeEnum.TRIANGLE_SMALL:
                return self.__trace_diagonal(origin, local_player_color, one_step=True)

            case PieceTypeEnum.SQUARE_LARGE:
                return self.__trace_orthogonal(origin, local_player_color)

            case PieceTypeEnum.SQUARE_SMALL:
                return self.__trace_orthogonal(
                    origin, local_player_color, one_step=True
                )

            case PieceTypeEnum.CIRCLE_LARGE:
                return self.__trace_diagonal(
                    origin, local_player_color
                ) + self.__trace_orthogonal(origin, local_player_color)

            case PieceTypeEnum.CIRCLE_SMALL:
                return self.__trace_diagonal(
                    origin, local_player_color, one_step=True
                ) + self.__trace_orthogonal(origin, local_player_color, one_step=True)

    @property
    def matrix(self) -> List[List[Piece | None]]:
        return self.__matrix

    def read(self, coordinates: Coordinates) -> Piece | None:
        return self.__matrix[coordinates.x][coordinates.y]

    def __get_checks(self, local_player_color: PieceColorEnum) -> list[Coordinates]:
        def filter_fn(c: Coordinates) -> bool:
            p = self.read(c)
            return p is not None and p.color != local_player_color

        y = 0 if local_player_color == PieceColorEnum.BLACK else Config.BOARD_SIZE - 1
        row = tuple(Coordinates(x, y) for x in range(Config.BOARD_SIZE))

        return list(filter(filter_fn, row))

    def __get_contestants(self, target: Coordinates) -> list[Coordinates]:
        target_piece = self.read(target)
        if target_piece is None:
            return

        target_color = target_piece.color
        contestants = []

        def filter_fn(c: Coordinates) -> bool:
            return self.read(c) is not None

        candidates: list[list[Coordinates]] = [
            list(
                filter(
                    filter_fn,
                    self.__trace_orthogonal(target, target_color, one_step=True),
                )
            ),
            list(
                filter(
                    filter_fn,
                    self.__trace_diagonal(target, target_color, one_step=True),
                )
            ),
            list(filter(filter_fn, self.__trace_orthogonal(target, target_color))),
            list(filter(filter_fn, self.__trace_diagonal(target, target_color))),
        ]

        reachers: list[list[PieceTypeEnum]] = [
            [
                PieceTypeEnum.SQUARE_LARGE,
                PieceTypeEnum.SQUARE_SMALL,
                PieceTypeEnum.CIRCLE_LARGE,
                PieceTypeEnum.CIRCLE_SMALL,
            ],
            [
                PieceTypeEnum.TRIANGLE_LARGE,
                PieceTypeEnum.TRIANGLE_SMALL,
                PieceTypeEnum.CIRCLE_LARGE,
                PieceTypeEnum.CIRCLE_SMALL,
            ],
            [
                PieceTypeEnum.SQUARE_LARGE,
                PieceTypeEnum.CIRCLE_LARGE,
            ],
            [
                PieceTypeEnum.TRIANGLE_LARGE,
                PieceTypeEnum.CIRCLE_LARGE,
            ],
        ]

        for idx, c_list in enumerate(candidates):
            possible_capture_types = reachers[idx]
            valid = list(
                filter(lambda c: self.read(c).type in possible_capture_types, c_list)
            )
            contestants += valid

        return contestants

    def __trace_diagonal(
        self,
        origin: Coordinates,
        local_player_color: PieceColorEnum,
        one_step: bool = False,
    ) -> list[Coordinates]:
        diagonals = []
        x, y = origin.x, origin.y
        transformers: list[Callable[[int, int], tuple[int]]] = [
            lambda x, y: (x - 1, y - 1),
            lambda x, y: (x - 1, y + 1),
            lambda x, y: (x + 1, y - 1),
            lambda x, y: (x + 1, y + 1),
        ]
        limiters: list[Callable[[int, int, int], bool]] = [
            lambda i, j, _: i >= 0 and j >= 0,
            lambda i, j, c: i >= 0 and j < c,
            lambda i, j, c: i < c and j >= 0,
            lambda i, j, c: i < c and j < c,
        ]

        for idx, t in enumerate(transformers):
            i, j = t(x, y)
            lmt = limiters[idx]
            while lmt(i, j, Config.BOARD_SIZE):
                c = Coordinates(i, j)
                piece = self.read(c)
                if piece is not None:
                    if piece.color != local_player_color:
                        diagonals.append(c)
                    break
                diagonals.append(c)
                if one_step:
                    break
                i, j = t(i, j)

        return diagonals

    def __trace_orthogonal(
        self,
        origin: Coordinates,
        local_player_color: PieceColorEnum,
        one_step: bool = False,
    ) -> list[Coordinates]:
        orthogonals = []
        x, y = origin.x, origin.y
        transformers = [
            lambda x, y: (x - 1, y),
            lambda x, y: (x + 1, y),
            lambda x, y: (x, y - 1),
            lambda x, y: (x, y + 1),
        ]
        limiters = [
            lambda i, _, __: i >= 0,
            lambda i, _, c: i < c,
            lambda _, j, __: j >= 0,
            lambda _, j, c: j < c,
        ]
        for idx, t in enumerate(transformers):
            i, j = t(x, y)
            lmt = limiters[idx]
            while lmt(i, j, Config.BOARD_SIZE):
                c = Coordinates(i, j)
                piece = self.read(c)
                if piece is not None:
                    if piece.color != local_player_color:
                        orthogonals.append(c)
                    break
                orthogonals.append(c)
                if one_step:
                    break
                i, j = t(i, j)

        return orthogonals
