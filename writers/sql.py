import datetime
import logging

from sqlalchemy import (
    URL,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.types import JSON
from typing import Any, Union

from writers import MetricsWriter

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class Metric(Base):
    __tablename__ = "metric"

    id: Mapped[int] = mapped_column(primary_key=True)
    probe: Mapped[str]
    version: Mapped[str]
    data: Mapped[dict] = mapped_column(type_=JSON)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())


class Sql(MetricsWriter):
    def __init__(self, connection: Union[str, URL]) -> None:
        super().__init__()

        self._engine = create_engine(connection)
        Base.metadata.create_all(self._engine)

    def output_metrics(self, probe: str, version: str, data: dict[str, Any]):
        logger.info(f"Writing metrics for probe {probe}@{version}")
        with Session(self._engine) as session:
            session.add(
                Metric(
                    probe=probe,
                    version=version,
                    data=data,
                )
            )
            session.commit()
