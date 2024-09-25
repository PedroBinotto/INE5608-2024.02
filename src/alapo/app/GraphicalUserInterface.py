from typing import Any, List
from alapo.app.Peca import Peca
from alapo.app.TipoPecaEnum import TipoPecaEnum
from alapo.app.config import Config
from alapo.app.meta.EventEnum import EventEnum
from alapo.app.meta.EventManager import EventManager
from tkinter import Tk, Canvas, Frame, Label
from itertools import cycle

from alapo.dog_fmw.dog.dog_interface import DogPlayerInterface
from alapo.dog_fmw.dog.start_status import StartStatus

class GraphicalUserInterface(DogPlayerInterface):
    def __init__(self):
        self.__colors = [Config.DARK, Config.LIGHT]
        self.__size = Config.BOARD_SIZE
        self.__eventManager = EventManager()
        self.__window = None
        self.__canvas = None

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
                position = current_state[j][i]
                if position is not None:
                    self.__draw_piece(i, j, position.tipo, black=j > 3)     # DEBUG


    def __draw_app(self) -> None:
        rightframe = Frame(self.__window)
        rightframe.grid(row=0, column=0, rowspan=10, padx=100)
        label = Label(rightframe, text="Game Menu", font=("Arial", 16))
        label.grid(row=0, column=0, pady=10)
        self.__draw_board()

    def __draw_board(self) -> None:
        self.__canvas = Canvas(self.__window, width=768, height=768)
        self.__canvas.grid(row=0, column=1, columnspan=8, rowspan=8)
        for i in range(self.__size):
            color = cycle(self.__colors[::-1] if not i % 2 else self.__colors)
            for j in range(self.__size):
                self.__draw_tile(i, j, color)

    def __draw_tile(self, i: int, j: int, color: cycle) -> None:
        args = self.__calculate_position(i, j)
        kwargs = { **self.__default_tk_kwargs(), **{ "fill": next(color), "tags":f"tile{i+1}{j+1}" } }
        self.__canvas.create_rectangle(*args, **kwargs)
        self.__bind_tag(i, j, "tile")

    def __draw_piece(self, i: int, j: int, tipo: TipoPecaEnum, black: bool) -> None:
        kwargs = {**self.__default_tk_kwargs(), **{"fill": "#000000" if black else "#FFFFFF", "tags":f"piece{i+1}{j+1}"}}
        match tipo:
            case TipoPecaEnum.TRIANGULAR_GRANDE:
                args = self.__resolve_triangle(i, j, False)
                self.__canvas.create_polygon(*args, **kwargs)
            case TipoPecaEnum.QUADRADA_GRANDE:
                self.__canvas.create_rectangle(*self.__calculate_position(i, j, True),**kwargs)
            case TipoPecaEnum.CIRCULAR_GRANDE:
                self.__canvas.create_oval(*self.__calculate_position(i, j, True),**kwargs)
            case TipoPecaEnum.TRIANGULAR_PEQUENA:
                args = self.__resolve_triangle(i, j, True)
                self.__canvas.create_polygon(*args, **kwargs)
            case TipoPecaEnum.QUADRADA_PEQUENA:
                self.__canvas.create_rectangle(*self.__calculate_position(i, j, True, True),**kwargs)
            case TipoPecaEnum.CIRCULAR_PEQUENA:
                self.__canvas.create_oval(*self.__calculate_position(i, j, True, True),**kwargs)
        self.__bind_tag(i, j, "piece")

    def __bind_tag(self, i: int, j: int, tag_prexfix: str):
        self.__canvas.tag_bind( f"{tag_prexfix}{i+1}{j+1}", "<Button-1>", lambda _,  i=i+1, j=j+1: self.receive_move({ "x": i, "y": j, })) # type: ignore[misc] 

    def __resolve_triangle(self, i: int, j: int, half_size: bool = False) -> tuple[int,int,int,int,int,int]:
        horizontal_padding = Config.BOARD_PADDING_SCALE * 3 if half_size else Config.BOARD_PADDING_SCALE
        vertical_padding = Config.BOARD_PADDING_SCALE * 4.5 if half_size else Config.BOARD_PADDING_SCALE
        defaults = self.__calculate_position(i, j, False)
        side_length = Config.BOARD_SCALE
        x1, y1 = defaults[0] + 45, defaults[1] + horizontal_padding
        x2, y2 = x1 - (side_length / 2) + horizontal_padding, y1 + (side_length * (3 ** 0.5) / 2) - vertical_padding
        x3, y3 = x1 + (side_length / 2) - horizontal_padding, y2 

        return (x1, y1, x2, y2, x3, y3)

    def __calculate_position(self, i: int, j: int, include_padding: bool = False, half_size: bool = False) -> tuple[int, int, int]:
        padding = (Config.BOARD_PADDING_SCALE * 2 if half_size else Config.BOARD_PADDING_SCALE) if include_padding else 0
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
