from abc import ABC, abstractmethod


class Probe(ABC):
    # @abstractstaticmethod
    # def arg_parser() -> argparse.ArgumentParser:
    #     raise NotImplementedError()

    @abstractmethod
    def poll(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def version(self) -> str:
        raise NotImplementedError()
