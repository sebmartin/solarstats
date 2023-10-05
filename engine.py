import logging
import pprint
import sys
import time

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
        self.frequency = frequency  # seconds
        self.probes = probes
        self.writers = writers

    def run(self):
        logger.info("=" * 80)
        logger.info("Starting probes. Press CTRL-C to terminate")
        while True:
            for probe in self.probes:
                try:
                    logger.info(f"Polling with probe {probe.__class__.__name__}")
                    data = probe.poll()
                    if not data:
                        continue

                    logging.debug("Collected data:\n" + pprint.pformat(data))
                    for writer in self.writers:
                        try:
                            logger.info(f"Writing to {writer.__class__.__name__}")
                            writer.output_metrics(
                                probe.__class__.__name__, probe.version(), data
                            )
                        except Exception as exc:
                            logger.exception(exc)
                except Exception as exc:
                    logger.exception(exc)

            # Force log buffers and stdout to flush before sleeping
            for handler in logger.handlers + logger.root.handlers:
                if hasattr(handler, "flush"):
                    logger.root.handlers[0].flush()
            sys.stdout.flush()
            time.sleep(self.frequency)
