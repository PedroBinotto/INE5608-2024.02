from dataclasses import dataclass
from enum import Enum, auto
from alapo.app.GraphicalUserInterface import GraphicalUserInterface
from alapo.app.Board import Board, BoardInput, Move
from alapo.app.Piece import PieceColorEnum
from alapo.app.config import Config
from alapo.app.meta.EventManager import EventData, EventManager, EventEnum
from alapo.dog_fmw.dog.dog_actor import DogActor
from alapo.dog_fmw.dog.start_status import StartStatus


@dataclass
class Player:
    id: str
    name: str
    # color: PieceColorEnum


class MatchStateEnum(Enum):
    NONE = auto()
    WAITING_REMOTE = auto()
    WAITING_SELECT_PIECE = auto()
    WAITING_SELECT_DEST = auto()
    CHECK = auto()
    FINISHED_BY_TIE = auto()
    FINISHED_BY_VICTORY = auto()


class Alapo:
    def __init__(self) -> None:
        self.__match_state: MatchStateEnum = None
        self.__local_buffer: BoardInput = None
        self.__local_player: Player = None
        self.__is_player_two: bool = None
        self.__remote_player: Player = None
        self.__eventManager = EventManager()
        self.__board = Board()
        self.__gui = GraphicalUserInterface()
        self.__dog_actor = DogActor()
        self.__setupSubscriptions()

    def start(self) -> None:
        def get_username() -> str:
            while True:
                name = self.__gui.get_username().strip()
                if len(name):
                    return name

        while True:
            initial_response = self.__dog_actor.initialize(get_username(), self.__gui)
            if self.__dog_actor.proxy.status == 2:
                break

        self.__match_state = MatchStateEnum.NONE
        self.__eventManager.post(EventEnum.RECEIVE_DOG_RESPONSE, initial_response)
        self.__gui.initialize()

    def __setupSubscriptions(self) -> None:
        self.__eventManager.subscribe(EventEnum.BOARD_INPUT, self.__process_board_click)
        self.__eventManager.subscribe(EventEnum.RECEIVE_MOVE, self.__receive_move)
        self.__eventManager.subscribe(EventEnum.START_MATCH, self.__initiate_start)
        self.__eventManager.subscribe(
            EventEnum.RECEIVE_START_MATCH, self.__receive_start
        )
        self.__eventManager.subscribe(
            EventEnum.RECEIVE_WITHDRAWAL, self.__receive_withdrawal
        )

    def __receive_start(self, event: EventData[StartStatus]):
        start_status = event.data
        self.__setup_match(start_status)

    def __initiate_start(self, _: EventData[None]):
        start_status = self.__dog_actor.start_match(2)
        self.__setup_match(start_status)

    def __setup_match(self, status: StartStatus) -> None:
        if not status.code == "2":
            self.__eventManager.post(EventEnum.SERVER_SIDE_ERR, status.get_message())
            return

        local_player = status.get_players()[0]
        remote_player = status.get_players()[1]

        self.__is_player_two = int(local_player[2]) == 2

        self.__local_player = Player(local_player[1], local_player[0])
        self.__remote_player = Player(remote_player[1], remote_player[0])

        if self.__is_player_two:
            self.__match_state = MatchStateEnum.WAITING_REMOTE
        else:
            self.__match_state = MatchStateEnum.WAITING_SELECT_PIECE

        self.__board.setup()
        self.__refresh()

        self.__gui.show_popup_message(
            f"Partida iniciada contra {self.__remote_player.name}!"
        )

    def __process_board_click(self, event: EventData[BoardInput]) -> None:
        if self.__is_player_two:
            input = BoardInput(**self.__rotate_input((event.data.x, event.data.y)))
        else:
            input = event.data

        if self.__match_state == MatchStateEnum.WAITING_SELECT_PIECE:
            self.__local_buffer = input
            self.__match_state = MatchStateEnum.WAITING_SELECT_DEST
        elif self.__match_state == MatchStateEnum.WAITING_SELECT_DEST:
            self.__register_move(Move(self.__local_buffer, input))
            self.__dog_actor.send_move(
                {
                    "origin": {"x": self.__local_buffer.x, "y": self.__local_buffer.y},
                    "destination": {
                        "x": input.x,
                        "y": input.y,
                    },
                }
            )

    def __receive_move(self, event: EventData[Move]):
        self.__register_move(event.data)

    def __validate_input(self, input: BoardInput):
        print("in position: ", f"x: {input.x}, y: {input.y}", self.__board.read(input))

    def __register_move(self, move: Move) -> None:
        self.__board.apply_move(move.origin, move.destination)
        self.__refresh()

    def __receive_withdrawal(self, _: EventData[None]) -> None:
        self.__gui.show_popup_message(f"Oponente {self.__remote_player.name} desistiu!")

    def __rotate_input(self, coordinates: tuple[int, int]) -> tuple[int, int]:
        i, j = coordinates
        n = Config.BOARD_SIZE

        return (n - 1 - i, n - 1 - j)

    def __rotate_matrix(self, matrix):
        n = Config.BOARD_SIZE
        rotated_matrix = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                new_i, new_j = self.__rotate_input((i, j))
                rotated_matrix[new_i][new_j] = matrix[i][j]
        return rotated_matrix

    def __refresh(self):
        self.__gui.update_board_display(
            self.__board.matrix
            if not self.__is_player_two
            else self.__rotate_matrix(self.__board.matrix)
        )
