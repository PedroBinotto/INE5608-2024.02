from typing import List
from alapo.app.Peca import CorPecaEnum, Peca, TipoPecaEnum
from alapo.app.config import Config
from alapo.app.meta.EventManager import EventManager, EventEnum
from tkinter import Button, Entry, Tk, Canvas, Frame, Label
from itertools import cycle

from alapo.dog_fmw.dog.dog_interface import DogPlayerInterface
from alapo.dog_fmw.dog.start_status import StartStatus


class GraphicalUserInterface(DogPlayerInterface):
    def __init__(self):
        self.__tile_colors = [Config.DARK, Config.LIGHT]
        self.__piece_colors = {
            CorPecaEnum.PRETO: Config.BLACK,
            CorPecaEnum.BRANCO: Config.WHITE
        }
        self.__size = Config.BOARD_SIZE
        self.__eventManager = EventManager()
        self.__window = None
        self.__canvas = None
        self.__username_field = None

    def initialize(self) -> None:
        self.__window = Tk()
        self.__window.title(Config.APP_NAME)
        self.__draw_app()
        self.__window.mainloop()

    def receive_start(self, start_status: StartStatus) -> None:
        self.__eventManager.post(EventEnum.RECEIVE_START_MATCH, start_status)

    def receive_move(self, a_move) -> None:
        self.__eventManager.post(EventEnum.RECEIVE_MOVE, a_move)

    def receive_withdrawal_notification(self) -> None:
        self.__eventManager.post(EventEnum.RECEIVE_WITHDRAWAL)

    def update(self, current_state: List[List[Peca | None]]) -> None:
        self.__canvas.delete("piece")
        for i in range(Config.BOARD_SIZE):
            for j in range(Config.BOARD_SIZE):
                peca = current_state[j][i]
                if peca is not None:
                    self.__draw_piece(i, j, peca.tipo, peca.cor)     # DEBUG

    def __draw_app(self) -> None:
        self.__draw_rpanel()
        self.__draw_board()

    def __draw_rpanel(self) -> None:
        rightframe = Frame(self.__window)
        rightframe.grid(row=0, column=0, rowspan=10, padx=100)

        label = Label(rightframe, text="Alapo", font=("Arial", 16))
        label.grid(row=0, column=0, pady=10, columnspan=2)

        username_label = Label(rightframe, text="Nome do jogador:", font=("Arial", 12))
        username_label.grid(row=1, column=0, padx=10, pady=10)

        self.__username_field = Entry(rightframe, font=("Arial", 12), width=20)
        self.__username_field.grid(row=1, column=1, padx=10, pady=10)

        start_button = Button(rightframe, text="Iniciar partida", font=("Arial", 12), command=self.receive_start)
        start_button.grid(row=2, column=0, columnspan=2, pady=20)

    def __draw_board(self) -> None:
        self.__canvas = Canvas(self.__window, width=568, height=568)
        self.__canvas.grid(row=0, column=1, columnspan=8, rowspan=8, pady=(0, 125))
        for i in range(self.__size):
            color = cycle(self.__tile_colors[::-1] if not i % 2 else self.__tile_colors)
            for j in range(self.__size):
                self.__draw_tile(i, j, color)

    def __draw_tile(self, i: int, j: int, color: cycle) -> None:
        tag_prefix = "tile"
        args = self.__calculate_position(i, j)
        kwargs = {**self.__default_tk_kwargs(), **{"fill": next(color), "tags": f"{tag_prefix}{i + 1}{j + 1}"}}
        self.__canvas.create_rectangle(*args, **kwargs)
        self.__bind_tag(i, j, tag_prefix)

    def __draw_piece(self, i: int, j: int, tipo: TipoPecaEnum, cor: CorPecaEnum) -> None:
        tag_prefix = "piece"
        kwargs = {**self.__default_tk_kwargs(),
                  **{"fill": self.__piece_colors[cor],
                     "tags": f"{tag_prefix}{i + 1}{j + 1}"}}
        match tipo:
            case TipoPecaEnum.TRIANGULAR_GRANDE:
                args = self.__resolve_triangle(i, j, False)
                self.__canvas.create_polygon(*args, **kwargs)
            case TipoPecaEnum.QUADRADA_GRANDE:
                self.__canvas.create_rectangle(*self.__calculate_position(i, j, True), **kwargs)
            case TipoPecaEnum.CIRCULAR_GRANDE:
                self.__canvas.create_oval(*self.__calculate_position(i, j, True), **kwargs)
            case TipoPecaEnum.TRIANGULAR_PEQUENA:
                args = self.__resolve_triangle(i, j, True)
                self.__canvas.create_polygon(*args, **kwargs)
            case TipoPecaEnum.QUADRADA_PEQUENA:
                self.__canvas.create_rectangle(*self.__calculate_position(i, j, True, True), **kwargs)
            case TipoPecaEnum.CIRCULAR_PEQUENA:
                self.__canvas.create_oval(*self.__calculate_position(i, j, True, True), **kwargs)
        self.__bind_tag(i, j, tag_prefix)

    def __bind_tag(self, i: int, j: int, tag_prexfix: str):
        self.__canvas.tag_bind(f"{tag_prexfix}{i + 1}{j + 1}", "<Button-1>", lambda _, i=i + 1,
                               j=j + 1: self.receive_move({"x": i, "y": j, }))  # type: ignore[misc]

    def __resolve_triangle(self,
                           i: int,
                           j: int,
                           half_size: bool = False) -> tuple[float,
                                                             float,
                                                             float,
                                                             float,
                                                             float,
                                                             float]:
        horizontal_padding = Config.BOARD_PADDING_SCALE * 3 if half_size else Config.BOARD_PADDING_SCALE
        vertical_padding = Config.BOARD_PADDING_SCALE * 5.1 if half_size else Config.BOARD_PADDING_SCALE
        defaults = self.__calculate_position(i, j, False)
        side_length = Config.BOARD_SCALE
        x1, y1 = defaults[0] + Config.BOARD_SCALE / 2, defaults[1] + horizontal_padding
        x2, y2 = x1 - (side_length / 2) + horizontal_padding, y1 + (side_length * (3 ** 0.5) / 2) - vertical_padding
        x3, y3 = x1 + (side_length / 2) - horizontal_padding, y2

        return (x1, y1, x2, y2, x3, y3)

    def __calculate_position(self, i: int, j: int, include_padding: bool = False,
                             half_size: bool = False) -> tuple[int, int, int, int]:
        padding = (Config.BOARD_PADDING_SCALE * 2
                   if half_size
                   else Config.BOARD_PADDING_SCALE) if include_padding else 0
        return (
            (i * Config.BOARD_SCALE) + padding,
            (((Config.BOARD_SIZE + 1) - j) * Config.BOARD_SCALE) + padding,
            (i * Config.BOARD_SCALE + Config.BOARD_SCALE) - padding,
            (((Config.BOARD_SIZE + 1) - j) * Config.BOARD_SCALE + Config.BOARD_SCALE) - padding
        )

    def __default_tk_kwargs(self) -> dict[str, str]:
        return {
            "fill": "#000000",
            "outline": ""
        }
