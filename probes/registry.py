from enum import Enum
from probes import Probe

from probes.renogy import RenogyRoverProbe


class ProbeType(Enum):
    RENOGY = "renogy"
    RENOGY_SIM = "renogy_sim"


ALL_PROBES: dict[ProbeType, type[Probe]] = {ProbeType.RENOGY: RenogyRoverProbe}

DEFAULT_PROBE = ProbeType.RENOGY
