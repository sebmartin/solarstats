import argparse
import logging
from os.path import abspath, dirname
from typing import Union

from config import ConfigNotFoundError, load_config
from engine import Engine
from probes.registry import ALL_PROBES, ALL_WRITERS

logger = logging.getLogger(__name__)


def set_logging(level: Union[int, str]):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",  # Define the date and time format
    )


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

    config_file = abspath(args.config) if args.config else DEFAULT_CONFIG_PATH

    try:
        config = load_config(config_file, probes=ALL_PROBES, writers=ALL_WRITERS)
        set_logging(logging.DEBUG if args.verbose else config.logging_level)
        logger.info(f"Loaded configuration from: {config_file}")
        logger.debug(f"Loaded configuration values:\n  {config}")

        engine = Engine(
            frequency=config.frequency, probes=config.probes, writers=config.writers
        )
        engine.run()
    except ConfigNotFoundError:
        logger.error(f"Could not find valid config file at: {config_file}")
    except KeyboardInterrupt:
        logger.info("Done")
