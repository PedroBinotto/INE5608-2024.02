from alapo.app.GraphicalUserInterface import GraphicalUserInterface
from alapo.app.Tabuleiro import Tabuleiro
from alapo.app.meta.EventEnum import EventEnum
from alapo.app.meta.EventManager import EventData, EventManager
from alapo.dog_fmw.dog.dog_actor import DogActor

class Alapo:
    def __init__(self) -> None:
        self.__eventManager = EventManager()
        self.__board = Tabuleiro()
        self.__gui = GraphicalUserInterface()
        self.__doc_actor = DogActor()
        self.__setupSubscriptions()

    def start(self) -> None:
        self.__doc_actor.initialize("fulano", self.__gui)
        self.__gui.initialize()

    def __setupSubscriptions(self) -> None:
        # self.__eventManager.subscribe(EventEnum.RECEIVE_START_MATCH , self.__setup_match) # DEBUG
        self.__eventManager.subscribe(EventEnum.RECEIVE_MOVE, self.__receive_move)
        self.__eventManager.subscribe(EventEnum.RECEIVE_MOVE, self.__setup_match)

    def __setup_match(self, _: EventData) -> None:
        self.__board.setup()
        self.__gui.update(self.__board.matrix)

    def __receive_move(self, event: EventData) -> None:
        position = event.data
        print("Alapo::__receive_move", position)
