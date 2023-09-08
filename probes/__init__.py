from enum import Enum

from probes.renogy_rover import RenogyRover


from abc import ABC, abstractmethod, abstractstaticmethod
import argparse


class Probe(ABC):
    @abstractstaticmethod
    def arg_parser() -> argparse.ArgumentParser:
        raise NotImplementedError()

    def __init__(self, args) -> None:
        super().__init__()

    @abstractmethod
    def poll(self) -> dict:
        raise NotImplementedError()


class ControllerType(Enum):
    RENOGY = "renogy"


ALL_CONTROLLERS: dict[ControllerType, type[Probe]] = {
    ControllerType.RENOGY: RenogyRover
}

DEFAULT_CONTROLLER = ControllerType.RENOGY
