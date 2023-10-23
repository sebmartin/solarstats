from probes import Probe
from probes.psutil import PSUtil

from probes.renogy import RenogyRover, RenogyRoverSimulator
from writers import MetricsWriter
from writers.http import Http
from writers.sql import Sql

ALL_PROBES: list[type[Probe]] = [RenogyRover, RenogyRoverSimulator, PSUtil]
ALL_WRITERS: list[type[MetricsWriter]] = [Sql, Http]
