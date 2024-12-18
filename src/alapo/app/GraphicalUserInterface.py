from alapo.app.Board import Coordinates, Matrix, Move
from alapo.app.Piece import PieceColorEnum, PieceTypeEnum
from alapo.app.config import Config
from alapo.app.meta.EventManager import EventData, EventManager, EventEnum
from tkinter import Button, Tk, Canvas, Frame, Label
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from itertools import cycle

from alapo.dog_fmw.dog.dog_interface import DogPlayerInterface
from alapo.dog_fmw.dog.start_status import StartStatus


class GraphicalUserInterface(DogPlayerInterface):
    def __init__(self):
        self.__start_button: Button = None
        self.__tile_colors: list[str] = [Config.DARK, Config.LIGHT]
        self.__piece_colors: dict[PieceColorEnum, str] = {
            PieceColorEnum.BLACK: Config.BLACK,
            PieceColorEnum.WHITE: Config.WHITE,
        }
        self.__size = Config.BOARD_SIZE
        self.__event_manager = EventManager()
        self.__window: Tk = None
        self.__canvas: Canvas = None
        self.__setup_subscriptions()

    def initialize(self) -> None:
        self.__window = Tk()
        self.__window.title(Config.APP_NAME)
        self.__draw_app()
        self.__window.mainloop()

    def get_username(self) -> str:
        return self.__show_prompt_message("Informe o nome do jogador:")

    def receive_start(self, start_status: StartStatus) -> None:
        self.set_start_button_state(False)
        self.__event_manager.post(EventEnum.RECEIVE_START_MATCH, start_status)

    def receive_move(self, a_move) -> None:
        move = self.__deserialize_move(a_move)
        if move:
            self.show_popup_message("Recebe movimento")
            self.__event_manager.post(EventEnum.RECEIVE_MOVE, move)
            return
        self.__finish_by_victory()

    def receive_withdrawal_notification(self) -> None:
        self.on_match_finish()
        self.__event_manager.post(EventEnum.RECEIVE_WITHDRAWAL)

    def update_board_display(self, board_state: Matrix) -> None:
        self.__canvas.delete("piece")
        for i in range(Config.BOARD_SIZE):
            for j in range(Config.BOARD_SIZE):
                peca = board_state[i][j]
                if peca is not None:
                    self.__draw_board_piece(i, j, peca.type, peca.color)  # DEBUG

    def show_popup_message(self, msg: str) -> None:
        showinfo(Config.APP_NAME, f"MENSAGEM: {msg}")

    def set_start_button_state(self, active: bool) -> None:
        self.__start_button["state"] = "normal" if active else "disabled"

    def __finish_by_victory(self) -> None:
        self.show_popup_message("Você venceu!")
        self.on_match_finish()

    def on_match_finish(self) -> None:
        self.set_start_button_state(True)
        self.clear_highlights()

    def __board_click(self, coordinates: Coordinates) -> None:
        self.__event_manager.post(EventEnum.BOARD_INPUT, coordinates)

    def __show_prompt_message(self, msg: str) -> str:
        return askstring(Config.APP_NAME, prompt=msg)

    def __draw_app(self) -> None:
        self.__draw_menu_panel()
        self.__draw_board_canvas()

    def __draw_menu_panel(self) -> None:
        def on_iniciar_partida(*_):
            self.set_start_button_state(False)
            self.__event_manager.post(EventEnum.START_MATCH)

        rightframe = Frame(self.__window)
        rightframe.grid(row=0, column=0, rowspan=10, padx=100)

        label = Label(rightframe, text="Alapo", font=("Arial", 16))
        label.grid(row=0, column=0, pady=10, columnspan=2)

        self.__start_button = Button(
            rightframe,
            text="Iniciar partida",
            font=("Arial", 12),
            command=on_iniciar_partida,
        )
        self.__start_button.grid(row=2, column=0, columnspan=2, pady=20)

    def __draw_board_canvas(self) -> None:
        self.__canvas = Canvas(self.__window, width=568, height=568)
        self.__canvas.grid(row=0, column=1, columnspan=8, rowspan=8, pady=(0, 125))
        for i in range(self.__size):
            color = cycle(self.__tile_colors[::-1] if not i % 2 else self.__tile_colors)
            for j in range(self.__size):
                self.__draw_board_tile(i, j, color)

    def __draw_board_tile(self, i: int, j: int, color: cycle) -> None:
        tag_prefix = "tile"
        args = self.__resolve_polygon_vertices(i, j)
        kwargs = {
            **self.__resolve_tk_kwargs(),
            **{"fill": next(color), "tags": f"{tag_prefix}{i}{j}"},
        }
        self.__canvas.create_rectangle(*args, **kwargs)
        self.__bind_button_tag(i, j, tag_prefix)

    def clear_highlights(self) -> None:
        self.__canvas.delete("highlight")

    def draw_board_highlight(self, i: int, j: int) -> None:
        tag_prefix = "highlight"
        args = self.__resolve_polygon_vertices(i, j)
        kwargs = {
            **self.__resolve_tk_kwargs(),
            **{
                "fill": "",
                "outline": "red",
                "width": 5,
                "tags": (f"{tag_prefix}{i}{j}", tag_prefix),
            },
        }
        self.__canvas.create_rectangle(*args, **kwargs)

    def __draw_board_piece(
        self, i: int, j: int, tipo: PieceTypeEnum, cor: PieceColorEnum
    ) -> None:
        def resolve_triange_vertices(
            i: int, j: int, half_size: bool = False
        ) -> tuple[float, float, float, float, float, float]:
            horizontal_padding = (
                Config.BOARD_PADDING_SCALE * 3
                if half_size
                else Config.BOARD_PADDING_SCALE
            )
            vertical_padding = (
                Config.BOARD_PADDING_SCALE * 5.1
                if half_size
                else Config.BOARD_PADDING_SCALE
            )
            defaults = self.__resolve_polygon_vertices(i, j, False)
            side_length = Config.BOARD_SCALE
            x1, y1 = (
                defaults[0] + Config.BOARD_SCALE / 2,
                defaults[1] + horizontal_padding,
            )
            x2, y2 = (
                x1 - (side_length / 2) + horizontal_padding,
                y1 + (side_length * (3**0.5) / 2) - vertical_padding,
            )
            x3, y3 = x1 + (side_length / 2) - horizontal_padding, y2

            return (x1, y1, x2, y2, x3, y3)

        tag_prefix = "piece"
        kwargs = {
            **self.__resolve_tk_kwargs(),
            **{
                "fill": self.__piece_colors[cor],
                "tags": (f"{tag_prefix}{i}{j}", tag_prefix),
            },
        }
        match tipo:
            case PieceTypeEnum.TRIANGLE_LARGE:
                args = resolve_triange_vertices(i, j, False)
                self.__canvas.create_polygon(*args, **kwargs)
            case PieceTypeEnum.SQUARE_LARGE:
                self.__canvas.create_rectangle(
                    *self.__resolve_polygon_vertices(i, j, True), **kwargs
                )
            case PieceTypeEnum.CIRCLE_LARGE:
                self.__canvas.create_oval(
                    *self.__resolve_polygon_vertices(i, j, True), **kwargs
                )
            case PieceTypeEnum.TRIANGLE_SMALL:
                args = resolve_triange_vertices(i, j, True)
                self.__canvas.create_polygon(*args, **kwargs)
            case PieceTypeEnum.SQUARE_SMALL:
                self.__canvas.create_rectangle(
                    *self.__resolve_polygon_vertices(i, j, True, True), **kwargs
                )
            case PieceTypeEnum.CIRCLE_SMALL:
                self.__canvas.create_oval(
                    *self.__resolve_polygon_vertices(i, j, True, True), **kwargs
                )
        self.__bind_button_tag(i, j, tag_prefix)

    def __bind_button_tag(self, i: int, j: int, tag_prexfix: str) -> None:
        self.__canvas.tag_bind(
            f"{tag_prexfix}{i}{j}",
            "<Button-1>",
            lambda _, i=i, j=j: self.__board_click(Coordinates(x=i, y=j)),
        )  # type: ignore[misc]

    def __resolve_polygon_vertices(
        self, i: int, j: int, include_padding: bool = False, half_size: bool = False
    ) -> tuple[int, int, int, int]:
        padding = (
            (
                Config.BOARD_PADDING_SCALE * 2
                if half_size
                else Config.BOARD_PADDING_SCALE
            )
            if include_padding
            else 0
        )
        return (
            (i * Config.BOARD_SCALE) + padding,
            (((Config.BOARD_SIZE + 1) - j) * Config.BOARD_SCALE) + padding,
            (i * Config.BOARD_SCALE + Config.BOARD_SCALE) - padding,
            (((Config.BOARD_SIZE + 1) - j) * Config.BOARD_SCALE + Config.BOARD_SCALE)
            - padding,
        )

    def __setup_subscriptions(self) -> None:
        def display_connection_notification(event: EventData[str]) -> None:
            self.show_popup_message(event.data)

        def on_error(_: EventData[str]) -> None:
            self.set_start_button_state(True)

        self.__event_manager.subscribe(
            EventEnum.RECEIVE_DOG_RESPONSE, display_connection_notification
        )
        self.__event_manager.subscribe(
            EventEnum.SERVER_SIDE_ERR, display_connection_notification
        )
        self.__event_manager.subscribe(EventEnum.SERVER_SIDE_ERR, on_error)

    def __resolve_tk_kwargs(self) -> dict[str, str]:
        return {"outline": ""}

    def __deserialize_move(self, move: dict) -> Move:
        if move["match_status"] == "next":
            return Move(
                Coordinates(move["origin"]["x"], move["origin"]["y"]),
                Coordinates(move["destination"]["x"], move["destination"]["y"]),
            )
        return None
