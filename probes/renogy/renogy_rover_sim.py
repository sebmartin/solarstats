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

    def __getattr__(self, key):
        """
        Intercept all methods from the parent class and return the metric data using the method
        name as the key.
        """
        metric = self.__get_next_record()
        if prop := metric.data.get(key):
            return prop
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{key}'"
        )

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