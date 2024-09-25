from typing import Protocol


class Process(Protocol):
    def start(self) -> None:
        ...
