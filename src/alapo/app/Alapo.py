from alapo.app.GraphicalUserInterface import GraphicalUserInterface
from alapo.app.Board import Board
from alapo.app.config import Config
from alapo.app.meta.EventManager import EventData, EventManager, EventEnum
from alapo.dog_fmw.dog.dog_actor import DogActor


class Alapo:
    def __init__(self) -> None:
        self.__eventManager = EventManager()
        self.__board = Board()
        self.__gui = GraphicalUserInterface()
        self.__doc_actor = DogActor()
        self.__setupSubscriptions()

    def start(self) -> None:
        self.__eventManager.post(
            EventEnum.RECEIVE_DOG_RESPONSE,
            {"msg": self.__doc_actor.initialize("fulano", self.__gui)},
        )
        self.__gui.initialize()

    def __setupSubscriptions(self) -> None:
        self.__eventManager.subscribe(EventEnum.RECEIVE_MOVE, self.__receive_move)
        self.__eventManager.subscribe(EventEnum.RECEIVE_START_MATCH, self.__setup_match)
        self.__eventManager.subscribe(
            EventEnum.RECEIVE_WITHDRAWAL, self.__receive_withdrawal
        )

    def __setup_match(self, _: EventData) -> None:
        Config.LOG_OUT("Alapo::__setup_match", "RECEIVE_START")
        self.__eventManager.post(
            EventEnum.RECEIVE_DOG_RESPONSE,
            {"msg": self.__doc_actor.start_match(2).get_message()},
        )
        self.__board.setup()
        self.__gui.update_board_display(self.__board.matrix)

    def __receive_move(self, event: EventData) -> None:
        Config.LOG_OUT("Alapo::__receive_move", "RECEIVE_MOVE")
        position = event.data
        Config.LOG_OUT("Alapo::__receive_move", position)

    def __receive_withdrawal(self, _: EventData) -> None:
        Config.LOG_OUT("Alapo::__receive_withdrawal", "RECEIVE_WITHDRAWAL")
