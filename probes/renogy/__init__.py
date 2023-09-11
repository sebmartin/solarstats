from probes import Probe
from probes.renogy.renogy_rover import RenogyRover


class RenogyRoverProbe(Probe):
    def __init__(self, controller: RenogyRover) -> None:
        super().__init__()

    def poll(self) -> dict:
        return {}
