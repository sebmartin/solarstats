from typing import Any
import pytest
from config import EngineConfig, load_config
from probes import Probe
from writers import MetricsWriter


def write_config(tmpdir, config: str):
    filepath = tmpdir / "config.yaml"
    with open(filepath, "w+") as fd:
        fd.write(config)
    return str(filepath)


@pytest.fixture
def probes():
    return []


@pytest.fixture
def writers():
    return []


class ReprHelper:
    def __repr__(self) -> str:
        args = [
            f"{a}={getattr(self, a)}"
            for a in dir(self)
            if not a.startswith("_") and not callable(getattr(self, a))
        ]
        return f"{self.__class__.__name__}({', '.join(args)})"


class Probe1(Probe, ReprHelper):
    def __init__(self, arg1: int) -> None:
        self.arg1 = arg1

    def poll(self) -> dict:
        return {}

    def __eq__(self, other: "Probe1") -> bool:
        return self.arg1 == other.arg1


class Probe2(Probe, ReprHelper):
    def __init__(self, arg2: str) -> None:
        self.arg2 = arg2

    def poll(self) -> dict:
        return {}

    def __eq__(self, other: "Probe2") -> bool:
        return self.arg2 == other.arg2


class Writer1(MetricsWriter, ReprHelper):
    def __init__(self, arg1: int, arg2: str) -> None:
        self.arg1 = arg1
        self.arg2 = arg2

    def output_metrics(self, provider: str, data: dict[str, Any]):
        pass

    def __eq__(self, other: "Writer1") -> bool:
        return self.arg1 == other.arg1 and self.arg2 == other.arg2


def test_load_config_with_probes_and_writer(tmpdir):
    config_yaml = """
frequency: 1.0
probes:
  probe1:
    arg1: 1
  probe2:
    arg2: two
writers:
  writer1:
    arg1: 1
    arg2: two
"""

    filepath = write_config(tmpdir, config_yaml)

    config = load_config(filepath, [Probe1, Probe2], [Writer1])
    assert config.frequency == 1.0
    assert config.probes == [Probe1(arg1=1), Probe2(arg2="two")]
    assert config.writers == [Writer1(arg1=1, arg2="two")]


def test_load_config_no_probes_no_writers(tmpdir, caplog):
    config_yaml = """
frequency: 1.0
probes:
  probe1_unknown:
    arg1: 1
  probe2_unknown:
    arg2: one
writers:
  writer1_unknown:
    arg1: 1
    arg2: two
"""

    filepath = write_config(tmpdir, config_yaml)

    config = load_config(filepath, [Probe1], [Writer1])
    assert config.frequency == 1.0
    assert config.probes == []
    assert config.writers == []

    assert (
        "Ignoring unknown probes from config: ['probe1_unknown', 'probe2_unknown']"
        in caplog.messages
    )
    assert "Available probe names are: ['Probe1']" in caplog.messages
    assert (
        "Ignoring unknown writers from config: ['writer1_unknown']" in caplog.messages
    )
    assert "Available writer names are: ['Writer1']" in caplog.messages


def test_load_config_defaults(tmpdir, probes, writers):
    filepath = write_config(tmpdir, "")
    config = load_config(filepath, probes, writers)
    assert config == EngineConfig()
