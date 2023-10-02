from unittest import mock
from unittest.mock import MagicMock

import pytest

from engine import Engine
from probes import Probe
from writers import MetricsWriter


class ProbeOne(Probe):
    pass


class ProbeTwo(Probe):
    pass


def test_engine_run_writes_metrics():
    probe1 = MagicMock(spec=ProbeOne)
    probe1.poll.side_effect = [{"metric1": 1.0}, {"metric1": 2.0}, KeyboardInterrupt]
    probe1.version.return_value = "1.1"
    probe2 = MagicMock(spec=ProbeTwo)
    probe2.poll.side_effect = [{"metric2": 10.0}, {"metric2": 20.0}]
    probe2.version.return_value = "1.2"
    writer1 = MagicMock(spec=MetricsWriter)
    writer2 = MagicMock(spec=MetricsWriter)

    engine = Engine(probes=[probe1, probe2], writers=[writer1, writer2], frequency=0.0)

    with pytest.raises(KeyboardInterrupt):
        engine.run()

    expected_writer_calls = [
        mock.call("ProbeOne", "1.1", {"metric1": 1.0}),
        mock.call("ProbeTwo", "1.2", {"metric2": 10.0}),
        mock.call("ProbeOne", "1.1", {"metric1": 2.0}),
        mock.call("ProbeTwo", "1.2", {"metric2": 20.0}),
    ]

    assert writer1.output_metrics.call_args_list == expected_writer_calls
    assert writer2.output_metrics.call_args_list == expected_writer_calls


@mock.patch("engine.logger")
def test_engine_run_continues_despite_writer_exceptions(mock_logger):
    probe = MagicMock(spec=ProbeOne)
    probe.poll.side_effect = [
        {"metric1": 1.0},
        {"metric1": 2.0},
        KeyboardInterrupt,
    ]
    probe.version.return_value = "1.1"
    exception = Exception("writer failure")
    writer = MagicMock(spec=MetricsWriter)
    writer.output_metrics.side_effect = [exception, None]

    engine = Engine(probes=[probe], writers=[writer], frequency=0.0)
    with pytest.raises(KeyboardInterrupt):
        engine.run()

    expected_writer_calls = [
        mock.call("ProbeOne", "1.1", {"metric1": 1.0}),
        mock.call("ProbeOne", "1.1", {"metric1": 2.0}),
    ]

    assert (
        writer.output_metrics.call_args_list == expected_writer_calls
    ), "both metrics should have been written despite the exception in between"
    mock_logger.exception.assert_called_with(exception)


@mock.patch("engine.logger")
def test_engine_run_continues_despite_polling_exceptions(mock_logger):
    exception = Exception("polling failure")
    probe = MagicMock(spec=ProbeOne)
    probe.poll.side_effect = [
        {"metric1": 1.0},
        exception,
        {"metric1": 2.0},
        KeyboardInterrupt,
    ]
    probe.version.return_value = "1.1"
    writer = MagicMock(spec=MetricsWriter)

    engine = Engine(probes=[probe], writers=[writer], frequency=0.0)
    with pytest.raises(KeyboardInterrupt):
        engine.run()

    expected_writer_calls = [
        mock.call("ProbeOne", "1.1", {"metric1": 1.0}),
        mock.call("ProbeOne", "1.1", {"metric1": 2.0}),
    ]

    assert (
        writer.output_metrics.call_args_list == expected_writer_calls
    ), "both metrics should have been written despite the exception in between"
    mock_logger.exception.assert_called_with(exception)
