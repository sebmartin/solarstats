from datetime import datetime, timedelta
from typing import Any, Generator
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from probes.renogy.renogy_rover import RenogyRoverController
from writers.sql import Metric


class RenogyRoverControllerSimulator(RenogyRoverController):
    """
    Simulate a real renogy controller by replaying metrics written to a database using the SQL writer.
    """

    def __init__(self, connection: str, poll_delay=None) -> None:
        self.__engine = create_engine(connection)
        self.__poll_delay: float = poll_delay or 1.0
        self.__stop_polling = False

    def stop_polling(self):
        self.__stop_polling = True

    def __get_next_record(self) -> Metric:
        return self.__generate_records().__next__()

    def __generate_records(self) -> Generator[Metric, Any, None]:
        with Session(self.__engine) as session:
            while not self.__stop_polling:
                metrics = session.scalars(
                    select(Metric).order_by(Metric.created_at.asc())
                )
                fetch_timestamp = datetime.utcnow()
                for metric in metrics:
                    while datetime.utcnow() - fetch_timestamp < timedelta(
                        seconds=self.__poll_delay
                    ):
                        yield metric

    def model(self):
        return self.__get_next_record().data.get("model")

    def system_voltage_current(self):
        return self.__get_next_record().data.get("system_voltage_current")

    def version(self):
        return self.__get_next_record().data.get("version")

    def serial_number(self):
        return self.__get_next_record().data.get("serial_number")

    def battery_percentage(self):
        return self.__get_next_record().data.get("battery_percentage")

    def battery_voltage(self):
        return self.__get_next_record().data.get("battery_voltage")

    def battery_temperature(self):
        return self.__get_next_record().data.get("battery_temperature")

    def controller_temperature(self):
        return self.__get_next_record().data.get("controller_temperature")

    def load_voltage(self):
        return self.__get_next_record().data.get("load_voltage")

    def load_current(self):
        return self.__get_next_record().data.get("load_current")

    def load_power(self):
        return self.__get_next_record().data.get("load_power")

    def solar_voltage(self):
        return self.__get_next_record().data.get("solar_voltage")

    def solar_current(self):
        return self.__get_next_record().data.get("solar_current")

    def solar_power(self):
        return self.__get_next_record().data.get("solar_power")

    def charging_amp_hours_today(self):
        return self.__get_next_record().data.get("charging_amp_hours_today")

    def discharging_amp_hours_today(self):
        return self.__get_next_record().data.get("discharging_amp_hours_today")

    def power_generation_today(self):
        return self.__get_next_record().data.get("power_generation_today")

    def charging_status(self):
        return self.__get_next_record().data.get("charging_status")

    def charging_status_label(self):
        return self.__get_next_record().data.get("charging_status_label")

    def battery_capacity(self):
        return self.__get_next_record().data.get("battery_capacity")

    def voltage_setting(self):
        return self.__get_next_record().data.get("voltage_setting")

    def battery_type(self):
        return self.__get_next_record().data.get("battery_type")
