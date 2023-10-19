import logging
from probes import Probe
from probes.renogy.renogy_rover import (
    RenogyRoverController,
)
from probes.renogy.renogy_rover_sim import RenogyRoverControllerSimulator

VERSION = "0.1"

logger = logging.getLogger(__name__)


class _RenogyRoverBase(Probe):
    def __init__(self, controller: RenogyRoverController) -> None:
        self._controller = controller

    def version(self) -> str:
        return VERSION

    def poll(self) -> dict:
        logger.info(f"Polling controller {self._controller.__class__.__name__}")
        return self._controller.all_data()


class RenogyRover(_RenogyRoverBase):
    def __init__(self, device, address, baudrate=9600, timeout=0.5) -> None:
        super().__init__(RenogyRoverController(device, address, baudrate, timeout))


class RenogyRoverSimulator(_RenogyRoverBase):
    def __init__(self, connection: str, poll_delay=None) -> None:
        super().__init__(
            RenogyRoverControllerSimulator(connection, poll_delay=poll_delay)
        )
