from probes import Probe

from probes.renogy import RenogyRoverProbe
from writers import MetricsWriter
from writers.http import HttpMetricsWriter
from writers.sql import SqlMetricsWriter

ALL_PROBES: list[type[Probe]] = [RenogyRoverProbe]
ALL_WRITERS: list[type[MetricsWriter]] = [SqlMetricsWriter, HttpMetricsWriter]
