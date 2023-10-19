from datetime import datetime, timedelta
import logging
from typing import Any, Generator, Union
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from probes.renogy.renogy_rover import RenogyRoverController
from probes.renogy.types import (
    BatteryType,
    ChargingMethod,
    ChargingModeController,
    ChargingState,
    Fault,
    LoadWorkingModes,
    OnOff,
    ProductType,
)
from writers.sql import Metric

logger = logging.getLogger(__name__)


class NoSimulatedMetricsFoundError(Exception):
    pass

class RenogyRoverControllerSimulator(RenogyRoverController):
    """
    Simulate a real renogy controller by replaying metrics written to a database using
    the SQL writer.
    """

    def __init__(self, connection: str, poll_delay=None) -> None:
        self.__engine = create_engine(connection)
        self.__poll_delay: float = poll_delay or 1.0
        self.__stop_polling = False
        self.__records = None

    def stop_polling(self):
        self.__stop_polling = True

    def __get_next_record(self) -> Metric:
        self.__records = self.__records or self.__generate_records()
        try:
            return self.__records.__next__()
        except StopIteration:
            logger.info("Restarting metrics generator")
            self.__records = self.__generate_records()
            try:
                return self.__records.__next__()
            except StopIteration:
                raise NoSimulatedMetricsFoundError("No metrics found in database")


    def __generate_records(self) -> Generator[Metric, Any, None]:
        with Session(self.__engine) as session:
            logger.info("Running query...")
            metrics = session.scalars(select(Metric).order_by(Metric.created_at.asc()))
            for metric in metrics:
                logging.debug(f"Returning metric: {metric.id}")
                fetch_timestamp = datetime.utcnow()
                while datetime.utcnow() - fetch_timestamp < timedelta(
                    seconds=self.__poll_delay
                ):
                    if self.__stop_polling:
                        return
                    yield metric

    def max_system_voltage(self) -> int:
        return self.__get_next_record().data.get("max_system_voltage") or 0

    def rated_charging_current(self) -> int:
        return self.__get_next_record().data.get("rated_charging_current") or 0

    def rated_discharging_current(self) -> int:
        return self.__get_next_record().data.get("rated_discharging_current") or 0

    def product_type(self) -> Union[ProductType, int]:
        return self.__get_next_record().data.get("product_type") or 0

    def product_model(self) -> str:
        return self.__get_next_record().data.get("product_model") or ""

    def software_version(self) -> str:
        return self.__get_next_record().data.get("software_version") or ""

    def hardware_version(self) -> str:
        return self.__get_next_record().data.get("hardware_version") or ""

    def serial_number(self) -> int:
        return self.__get_next_record().data.get("serial_number") or 0

    def device_address(self) -> int:
        return self.__get_next_record().data.get("device_address") or 0

    def battery_percentage(self) -> int:
        return self.__get_next_record().data.get("battery_percentage") or 0

    def battery_voltage(self) -> float:
        return self.__get_next_record().data.get("battery_voltage") or 0

    def charging_current(self) -> float:
        return self.__get_next_record().data.get("charging_current") or 0

    def controller_temperature(self) -> int:
        return self.__get_next_record().data.get("controller_temperature") or 0

    def battery_temperature(self) -> int:
        return self.__get_next_record().data.get("battery_temperature") or 0

    def load_voltage(self) -> float:
        return self.__get_next_record().data.get("load_voltage") or 0

    def load_current(self) -> float:
        return self.__get_next_record().data.get("load_current") or 0

    def load_power(self) -> int:
        return self.__get_next_record().data.get("load_power") or 0

    def solar_voltage(self) -> float:
        return self.__get_next_record().data.get("solar_voltage") or 0

    def solar_current(self) -> float:
        return self.__get_next_record().data.get("solar_current") or 0

    def charging_power(self) -> int:
        return self.__get_next_record().data.get("charging_power") or 0

    def battery_min_voltage_today(self) -> float:
        return self.__get_next_record().data.get("battery_min_voltage_today") or 0

    def battery_max_voltage_today(self) -> float:
        return self.__get_next_record().data.get("battery_max_voltage_today") or 0

    def max_charging_current_today(self) -> float:
        return self.__get_next_record().data.get("max_charging_current_today") or 0

    def max_discharging_current_today(self) -> float:
        return self.__get_next_record().data.get("max_discharging_current_today") or 0

    def max_charging_power_today(self) -> int:
        return self.__get_next_record().data.get("max_charging_power_today") or 0

    def max_discharging_power_today(self) -> int:
        return self.__get_next_record().data.get("max_discharging_power_today") or 0

    def charging_amphours_today(self) -> int:
        return self.__get_next_record().data.get("charging_amphours_today") or 0

    def discharging_amphours_today(self) -> int:
        return self.__get_next_record().data.get("discharging_amphours_today") or 0

    def power_generation_today(self) -> float:
        return self.__get_next_record().data.get("power_generation_today") or 0

    def power_consumption_today(self) -> float:
        return self.__get_next_record().data.get("power_consumption_today") or 0

    def total_operating_days(self) -> int:
        return self.__get_next_record().data.get("total_operating_days") or 0

    def total_battery_over_discharges(self) -> int:
        return self.__get_next_record().data.get("total_battery_over_discharges") or 0

    def total_battery_full_charges(self) -> int:
        return self.__get_next_record().data.get("total_battery_full_charges") or 0

    def total_battery_charge_amphours(self) -> int:
        return self.__get_next_record().data.get("total_battery_charge_amphours") or 0

    def total_battery_discharge_amphours(self) -> int:
        return (
            self.__get_next_record().data.get("total_battery_discharge_amphours") or 0
        )

    def cumulative_power_generation(self) -> float:
        return self.__get_next_record().data.get("cumulative_power_generation") or 0

    def cumulative_power_consumption(self) -> float:
        return self.__get_next_record().data.get("cumulative_power_consumption") or 0

    def set_street_light(self, state: OnOff):
        pass

    def street_light_status(self) -> Union[OnOff, None]:
        return self.__get_next_record().data.get("street_light_status")

    def set_street_light_brightness(self, intensity: int):
        return self.__get_next_record().data.get("set_street_light_brightness") or 0

    def street_light_brightness(self) -> int:
        return self.__get_next_record().data.get("street_light_brightness") or 0

    def charging_state(self) -> Union[ChargingState, None]:
        return self.__get_next_record().data.get("charging_state")

    def controller_fault_information(self) -> list[Fault]:
        return self.__get_next_record().data.get("controller_fault_information") or []

    def nominal_battery_capacity(self) -> int:
        return self.__get_next_record().data.get("nominal_battery_capacity") or 0

    def system_voltage_setting(self) -> int:
        return self.__get_next_record().data.get("system_voltage_setting") or 0

    def recognized_voltage(self) -> int:
        return self.__get_next_record().data.get("recognized_voltage") or 0

    def battery_type(self) -> Union[BatteryType, None]:
        return self.__get_next_record().data.get("battery_type")

    def over_voltage_threshold(self) -> int:
        return self.__get_next_record().data.get("over_voltage_threshold") or 0

    def charging_voltage_limit(self) -> int:
        return self.__get_next_record().data.get("charging_voltage_limit") or 0

    def equalizing_charging_voltage(self) -> int:
        return self.__get_next_record().data.get("equalizing_charging_voltage") or 0

    def boost_charging_voltage(self) -> int:
        return self.__get_next_record().data.get("boost_charging_voltage") or 0

    def floating_voltage(self) -> int:
        return self.__get_next_record().data.get("floating_voltage") or 0

    def boost_charging_recovery_voltage(self) -> int:
        return self.__get_next_record().data.get("boost_charging_recovery_voltage") or 0

    def over_discharge_recovery_voltage(self) -> int:
        return self.__get_next_record().data.get("over_discharge_recovery_voltage") or 0

    def under_voltage_warning_level(self) -> int:
        return self.__get_next_record().data.get("under_voltage_warning_level") or 0

    def over_discharge_voltage(self) -> int:
        return self.__get_next_record().data.get("over_discharge_voltage") or 0

    def discharging_limit_voltage(self) -> int:
        return self.__get_next_record().data.get("discharging_limit_voltage") or 0

    def end_of_charge_soc(self) -> int:
        return self.__get_next_record().data.get("end_of_charge_soc") or 0

    def end_of_discharge_soc(self) -> int:
        return self.__get_next_record().data.get("end_of_discharge_soc") or 0

    def over_discharge_time_delay(self) -> int:
        return self.__get_next_record().data.get("over_discharge_time_delay") or 0

    def equalizing_charging_time(self) -> int:
        return self.__get_next_record().data.get("equalizing_charging_time") or 0

    def boost_charging_time(self) -> int:
        return self.__get_next_record().data.get("boost_charging_time") or 0

    def equalizing_charging_interval(self) -> int:
        return self.__get_next_record().data.get("equalizing_charging_interval") or 0

    def temperature_compensation_factor(self) -> int:
        return self.__get_next_record().data.get("temperature_compensation_factor") or 0

    def first_stage_operating_duration(self) -> int:
        return self.__get_next_record().data.get("first_stage_operating_duration") or 0

    def first_stage_operating_power(self) -> int:
        return self.__get_next_record().data.get("first_stage_operating_power") or 0

    def second_stage_operating_duration(self) -> int:
        return self.__get_next_record().data.get("second_stage_operating_duration") or 0

    def second_stage_operating_power(self) -> int:
        return self.__get_next_record().data.get("second_stage_operating_power") or 0

    def third_stage_operating_duration(self) -> int:
        return self.__get_next_record().data.get("third_stage_operating_duration") or 0

    def third_stage_operating_power(self) -> int:
        return self.__get_next_record().data.get("third_stage_operating_power") or 0

    def morning_on_operating_duration(self) -> int:
        return self.__get_next_record().data.get("morning_on_operating_duration") or 0

    def morning_on_operating_power(self) -> int:
        return self.__get_next_record().data.get("morning_on_operating_power") or 0

    def load_working_mode(self) -> Union[LoadWorkingModes, None]:
        return self.__get_next_record().data.get("load_working_mode")

    def light_control_delay(self) -> int:
        return self.__get_next_record().data.get("light_control_delay") or 0

    def light_control_voltate(self) -> int:
        return self.__get_next_record().data.get("light_control_voltate") or 0

    def led_load_current_setting(self) -> float:
        return self.__get_next_record().data.get("led_load_current_setting") or 0

    def charging_mode_controlled_by(self) -> Union[ChargingModeController, None]:
        return self.__get_next_record().data.get("charging_mode_controlled_by")

    def special_power_control_state(self) -> Union[OnOff, None]:
        return self.__get_next_record().data.get("special_power_control_state")

    def each_night_on_function_state(self) -> Union[OnOff, None]:
        return self.__get_next_record().data.get("each_night_on_function_state")

    def no_charging_below_freezing(self) -> Union[OnOff, None]:
        return self.__get_next_record().data.get("no_charging_below_freezing")

    def charging_method(self) -> Union[ChargingMethod, None]:
        return self.__get_next_record().data.get("charging_method")
