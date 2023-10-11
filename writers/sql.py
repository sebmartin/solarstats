import datetime

from sqlalchemy import (
    URL,
    create_engine,
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
    def __init__(self, connection: str | URL) -> None:
        super().__init__()

        self._engine = create_engine(connection)
        Base.metadata.create_all(self._engine)

    def output_metrics(self, provider: str, version: str, data: dict[str, Any]):
        with Session(self._engine) as session:
            session.add(
                Metric(
                    provider=provider,
                    version=version,
                    data=data,
                )
            )
            session.commit()
