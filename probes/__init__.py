from abc import ABC, abstractmethod
from enum import Enum


class Probe(ABC):
    # @abstractstaticmethod
    # def arg_parser() -> argparse.ArgumentParser:
    #     raise NotImplementedError()

    @abstractmethod
    def poll(self) -> dict:
        raise NotImplementedError()
