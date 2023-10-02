import datetime

from sqlalchemy import (
    Engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.types import JSON
from traitlets import Any

from writers import MetricsWriter


class Base(DeclarativeBase):
    pass


class Metric(Base):
    __tablename__ = "metric"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str]
    version: Mapped[str]
    data: Mapped[dict] = mapped_column(type_=JSON)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())


class SqlMetricsWriter(MetricsWriter):
    def __init__(self, engine: Engine) -> None:
        super().__init__()

        self.__engine = engine
        Base.metadata.create_all(engine)

    def output_metrics(self, provider: str, version: str, data: dict[str, Any]):
        with Session(self.__engine) as session:
            session.add(
                Metric(
                    provider=provider,
                    version=version,
                    data=data,
                )
            )
            session.commit()
