from abc import ABC, abstractmethod, abstractstaticmethod
import argparse


class ProbeX(ABC):
    @abstractstaticmethod
    def arg_parser() -> argparse.ArgumentParser:
        raise NotImplementedError()

    def __init__(self, args) -> None:
        super().__init__()

    @abstractmethod
    def poll(self) -> dict:
        raise NotImplementedError()
