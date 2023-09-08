from datetime import datetime, timedelta
import pytest
from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session

from writers.sql import Metric, SqlMetricsWriter


@pytest.fixture
def engine():
    return create_engine("sqlite+pysqlite:///:memory:", echo=True)


@pytest.fixture
def conn(engine):
    with engine.connect() as c:
        yield c


@pytest.fixture
def writer(engine: Engine):
    return SqlMetricsWriter(engine)


def test_output_metrics(writer: SqlMetricsWriter, engine):
    provider = "test_provider"
    data = {"metric1": 1.0, "metric2": "pass", "metric3": False}

    created_threshold = datetime.utcnow()
    writer.output_metrics(provider, data)

    with Session(engine) as session:
        metric = session.scalar(select(Metric).limit(1))

    assert metric is not None
    assert metric.provider == provider
    assert metric.data == data
    assert metric.created_at - created_threshold < timedelta(seconds=2)
