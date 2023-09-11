import time
import logging

from probes import Probe
from writers import MetricsWriter

logger = logging.getLogger(__name__)


class Engine:
    def __init__(
        self,
        probes: list[Probe] = [],
        writers: list[MetricsWriter] = [],
        frequency: float = 1.0,
    ) -> None:
        self.frequency = frequency or 1.0  # seconds
        self.probes = probes
        self.writers = writers

    def run(self):
        while True:
            for probe in self.probes:
                try:
                    logger.info(f"Probing {probe}")
                    data = probe.poll()
                    if not data:
                        continue
                    for writer in self.writers:
                        try:
                            logger.info(f"Writing to {writer}")
                            writer.output_metrics(probe.__class__.__name__, data)
                        except Exception as exc:
                            logger.exception(exc)
                except Exception as exc:
                    logger.exception(exc)

            time.sleep(self.frequency)
