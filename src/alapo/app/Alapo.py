from alapo.app.GraphicalUserInterface import GraphicalUserInterface
from alapo.app.meta.EventManager import EventManager
from alapo.dog_fmw.dog.dog_actor import DogActor

class Alapo():
    def __init__(self) -> None:
        self.__name = "name!"
        self.__eventManager = EventManager()
        self.__gui = GraphicalUserInterface()
        self.__doc_actor = DogActor()
        self.__setupSubscriptions()

    def start(self) -> None:
        self.__doc_actor.initialize("fulano", self.__gui)
        self.__gui.initialize()

    def __setupSubscriptions(self) -> None:
        pass
