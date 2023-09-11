import argparse
import logging
from os.path import abspath, dirname

from config import ConfigNotFoundError, load_config
from engine import Engine
from probes import Probe
from probes.registry import ALL_PROBES, ALL_WRITERS
from writers import MetricsWriter
from writers.http import HttpMetricsWriter
from writers.sql import SqlMetricsWriter

logging.basicConfig()
logging.getLogger().setLevel("INFO")

logger = logging.getLogger(__name__)


def set_logging(level: str):
    logging.getLogger().setLevel(level)


DEFAULT_CONFIG_PATH = f"{dirname(abspath(__file__))}/config/config.yaml"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument(
        "-c",
        "--config",
        help=f"Path to config file. See config/README.md for more information. Defaults to {DEFAULT_CONFIG_PATH}",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Make output verbose"
    )
    args = parser.parse_args()

    if args.verbose:
        set_logging("DEBUG")

    config_file = abspath(args.config) if args.config else DEFAULT_CONFIG_PATH

    try:
        config = load_config(config_file, probes=ALL_PROBES, writers=ALL_WRITERS)
        logger.debug(f"Loaded configuration values:\n  {config}")

        engine = Engine(
            frequency=config.frequency, probes=config.probes, writers=config.writers
        )
        engine.run()
    except ConfigNotFoundError:
        logger.error(f"Could not find valid config file at: {config_file}")
    except KeyboardInterrupt:
        logger.info("Done")
