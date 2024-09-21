from typing import Any
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

    def __draw_app(self) -> None:
        self.__draw_board()
        rightframe = Frame(self.__window)
        rightframe.grid(row=0, column=0, rowspan=10, padx=100)
        label = Label(rightframe, text="Game Menu", font=("Arial", 16))
        label.grid(row=0, column=0, pady=10)

    def __draw_board(self) -> None:
        canvas = Canvas(self.__window, width=768, height=768)
        canvas.grid(row=0, column=1, columnspan=8, rowspan=8)
        board: list[list[Any]] = [[None for _ in range(self.__size)] for _ in range(self.__size)]

        for i in range(self.__size):
            color = cycle(self.__colors[::-1] if not i % 2 else self.__colors)
            for j in range(self.__size):
                x1 = i * 90
                y1 = (7-j) * 90
                x2 = x1 + 90
                y2 = y1 + 90
                board[j][i] = canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=next(color),
                    tags=f"tile{i+1}{j+1}",
                    outline=""
                )
                canvas.tag_bind(
                    f"tile{i+1}{j+1}","<Button-1>", 
                    lambda e,  # type: ignore[misc]
                    i=i+1,
                    j=j+1: self.receive_move({
                        "e": e,
                        "x": i,
                        "y": j,
                    })
                )

