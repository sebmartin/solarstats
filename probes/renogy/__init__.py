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
        return {
            "model": self._controller.model(),
            "system_voltage_current": self._controller.system_voltage_current(),
            "version": self._controller.version(),
            "serial_number": self._controller.serial_number(),
            "battery_percentage": self._controller.battery_percentage(),
            "battery_voltage": self._controller.battery_voltage(),
            "battery_temperature": self._controller.battery_temperature(),
            "controller_temperature": self._controller.controller_temperature(),
            "load_voltage": self._controller.load_voltage(),
            "load_current": self._controller.load_current(),
            "load_power": self._controller.load_power(),
            "solar_voltage": self._controller.solar_voltage(),
            "solar_current": self._controller.solar_current(),
            "solar_power": self._controller.solar_power(),
            "charging_amp_hours_today": self._controller.charging_amp_hours_today(),
            "discharging_amp_hours_today": self._controller.discharging_amp_hours_today(),
            "power_generation_today": self._controller.power_generation_today(),
            "charging_status": self._controller.charging_status(),
            "charging_status_label": self._controller.charging_status_label(),
            "battery_capacity": self._controller.battery_capacity(),
            "voltage_setting": self._controller.voltage_setting(),
            "battery_type": self._controller.battery_type(),
        }


class RenogyRover(_RenogyRoverBase):
    def __init__(self, device, address, baudrate=9600, timeout=0.5) -> None:
        super().__init__(RenogyRoverController(device, address, baudrate, timeout))


class RenogyRoverSimulator(_RenogyRoverBase):
    def __init__(self, connection: str, poll_delay=None) -> None:
        super().__init__(
            RenogyRoverControllerSimulator(connection, poll_delay=poll_delay)
        )
