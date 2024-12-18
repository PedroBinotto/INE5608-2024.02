from dataclasses import dataclass
from enum import Enum, auto
from alapo.app.GraphicalUserInterface import GraphicalUserInterface
from alapo.app.Board import Board, Coordinates, Matrix, Move
from alapo.app.Piece import PieceColorEnum
from alapo.app.config import Config
from alapo.app.meta.EventManager import EventData, EventManager, EventEnum
from alapo.dog_fmw.dog.dog_actor import DogActor
from alapo.dog_fmw.dog.start_status import StartStatus


@dataclass
class Player:
    id: str
    name: str
    color: PieceColorEnum


class MatchStateEnum(Enum):
    NONE = auto()
    WAITING_REMOTE = auto()
    WAITING_SELECT_PIECE = auto()
    WAITING_SELECT_DEST = auto()
    FINISHED_BY_VICTORY = auto()


class Alapo:
    def __init__(self) -> None:
        self.__match_state: MatchStateEnum = None
        self.__local_buffer: Coordinates = None
        self.__is_player_two: bool = None
        self.__local_player: Player = None
        self.__remote_player: Player = None
        self.__event_manager = EventManager()
        self.__board = Board()
        self.__gui = GraphicalUserInterface()
        self.__dog_actor = DogActor()
        self.__setup_subscriptions()

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
        self.__event_manager.post(EventEnum.RECEIVE_DOG_RESPONSE, initial_response)
        self.__gui.initialize()

    def __setup_subscriptions(self) -> None:
        self.__event_manager.subscribe(
            EventEnum.BOARD_INPUT, self.__process_board_click
        )
        self.__event_manager.subscribe(EventEnum.RECEIVE_MOVE, self.__receive_move)
        self.__event_manager.subscribe(EventEnum.START_MATCH, self.__initiate_start)
        self.__event_manager.subscribe(
            EventEnum.RECEIVE_START_MATCH, self.__receive_start
        )
        self.__event_manager.subscribe(
            EventEnum.RECEIVE_WITHDRAWAL, self.__receive_withdrawal
        )

    def __receive_start(self, event: EventData[StartStatus]) -> None:
        start_status = event.data
        self.__setup_match(start_status)

    def __initiate_start(self, _: EventData[None]) -> None:
        start_status = self.__dog_actor.start_match(2)
        self.__setup_match(start_status)

    def __setup_match(self, status: StartStatus) -> None:
        if not status.code == "2":
            self.__event_manager.post(EventEnum.SERVER_SIDE_ERR, status.get_message())
            return

        local_player = status.get_players()[0]
        remote_player = status.get_players()[1]

        self.__is_player_two = int(local_player[2]) == 2

        if self.__is_player_two:
            self.__match_state = MatchStateEnum.WAITING_REMOTE
            color = PieceColorEnum.WHITE
            opp_color = PieceColorEnum.BLACK
        else:
            self.__match_state = MatchStateEnum.WAITING_SELECT_PIECE
            color = PieceColorEnum.BLACK
            opp_color = PieceColorEnum.WHITE

        self.__local_player = Player(local_player[1], local_player[0], color)
        self.__remote_player = Player(remote_player[1], remote_player[0], opp_color)

        self.__board.setup()
        self.__refresh()

        if not self.__is_player_two:
            self.__highlight_pieces(
                self.__board.get_available_pieces(self.__local_player.color)
            )

        self.__gui.show_popup_message(
            f"Partida iniciada contra {self.__remote_player.name}!"
        )

    def __process_board_click(self, event: EventData[Coordinates]) -> None:
        if self.__is_player_two:
            input = self.__rotate_input(event.data)
        else:
            input = event.data

        if self.__match_state == MatchStateEnum.WAITING_SELECT_PIECE:
            if input not in self.__board.get_available_pieces(
                self.__local_player.color
            ):
                return

            self.__local_buffer = input
            self.__match_state = MatchStateEnum.WAITING_SELECT_DEST
            self.__highlight_destinations(input)
        elif self.__match_state == MatchStateEnum.WAITING_SELECT_DEST:
            if input not in self.__board.get_available_destinations(
                self.__local_buffer, self.__local_player.color
            ):
                return

            self.__gui.clear_highlights()
            move = Move(self.__local_buffer, input)
            self.__register_move(move)
            self.__dog_actor.send_move(self.__serialize_move(move))
            self.__match_state = MatchStateEnum.WAITING_REMOTE

    def __receive_move(self, event: EventData[Move]) -> None:
        self.__register_move(event.data)
        positions = self.__board.get_available_pieces(self.__local_player.color)

        if not len(positions):
            self.__match_state = MatchStateEnum.FINISHED_BY_VICTORY
            self.__communicate_loss()
            return

        self.__match_state = MatchStateEnum.WAITING_SELECT_PIECE
        self.__highlight_pieces(positions)

    def __highlight_destinations(self, origin: Coordinates) -> None:
        self.__gui.clear_highlights()
        for position in self.__board.get_available_destinations(
            origin, self.__local_player.color
        ):
            x, y = position.x, position.y
            if self.__is_player_two:
                new_coords = self.__rotate_input(Coordinates(x, y))
                x, y = new_coords.x, new_coords.y
            self.__gui.draw_board_highlight(x, y)

    def __highlight_pieces(self, positions: list[Coordinates]) -> None:
        self.__gui.clear_highlights()
        for position in positions:
            if self.__is_player_two:
                new_coordinates = self.__rotate_input(position)
                x, y = new_coordinates.x, new_coordinates.y
            else:
                x, y = position.x, position.y

            self.__gui.draw_board_highlight(x, y)

    def __register_move(self, move: Move) -> None:
        self.__board.apply_move(move)
        self.__refresh()

    def __communicate_loss(self) -> None:
        self.__gui.show_popup_message(f"Oponente {self.__remote_player.name} venceu!")
        self.__gui.on_match_finish()
        self.__dog_actor.send_move(
            {
                "match_status": "finished",
            }
        )

    def __receive_withdrawal(self, _: EventData[None]) -> None:
        self.__match_state = MatchStateEnum.NONE
        self.__gui.show_popup_message(f"Oponente {self.__remote_player.name} desistiu!")

    def __rotate_input(self, coordinates: Coordinates) -> Coordinates:
        i, j = coordinates.x, coordinates.y
        n = Config.BOARD_SIZE

        return Coordinates(n - 1 - i, n - 1 - j)

    def __rotate_matrix(self, matrix: Matrix) -> Matrix:
        n = Config.BOARD_SIZE
        rotated_matrix = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                new_coordinates = self.__rotate_input(Coordinates(i, j))
                new_i, new_j = new_coordinates.x, new_coordinates.y
                rotated_matrix[new_i][new_j] = matrix[i][j]
        return rotated_matrix

    def __refresh(self) -> None:
        self.__gui.update_board_display(
            self.__board.matrix
            if not self.__is_player_two
            else self.__rotate_matrix(self.__board.matrix)
        )

    def __serialize_move(self, move: Move) -> dict:
        return {
            "match_status": "next",
            "origin": {"x": move.origin.x, "y": move.origin.y},
            "destination": {
                "x": move.destination.x,
                "y": move.destination.y,
            },
        }
