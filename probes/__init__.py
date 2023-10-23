from abc import ABC, abstractmethod


class Probe(ABC):
    @abstractmethod
    def poll(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def version(self) -> str:
        raise NotImplementedError()
