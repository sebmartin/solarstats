import logging
import os
from dataclasses import dataclass, field
from typing import Union

import yaml

from probes import Probe
from writers import MetricsWriter

try:
    from yaml import CLoader as Loader  # noqa
except ImportError:
    from yaml import Loader  # noqa

logger = logging.getLogger(__name__)

@dataclass
class LoggingConfig:
    level: Union[int, str] = logging.WARNING
    filename: Union[str, None] = None

@dataclass
class EngineConfig:
    frequency: float = 30.0
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    probes: list[Probe] = field(default_factory=list)
    writers: list[MetricsWriter] = field(default_factory=list)


class ConfigNotFoundError(Exception):
    pass


def load_config(
    filepath: str, probes: list[type[Probe]], writers: list[type[MetricsWriter]]
) -> EngineConfig:
    if not os.path.exists(filepath):
        raise ConfigNotFoundError(filepath)

    logger.info(f"Loading config file: {filepath}")
    with open(filepath, "r") as fd:
        try:
            config = yaml.load(fd, Loader)
            if not isinstance(config, dict):
                config = {}
        except Exception:
            config = {}

    if not config:
        return EngineConfig()

    # configure logging
    if "logging" in config and isinstance(config["logging"], dict):
        config["logging"] = LoggingConfig(**config["logging"])

    # configure probes
    config_probes = set(config.get("probes", {}).keys())
    available_probes = {p.__name__ for p in probes}
    available_probes_lower = {p.__name__.lower() for p in probes}
    unknown_probes = {
        p for p in config_probes if p.lower() not in available_probes_lower
    }
    if unknown_probes:
        logger.warning(f"Ignoring unknown probes from config: {sorted(unknown_probes)}")
        logger.warning(f"Available probe names are: {sorted(available_probes)}")

    probes_map = {p.__name__.lower(): p for p in probes}
    config["probes"] = [
        probes_map[name.lower()](**probe)
        for name, probe in config.get("probes", {}).items()
        if name.lower() in probes_map
    ]
    configured_probes = sorted(p.__class__.__name__ for p in config["probes"])
    logger.info(f"Configured probes: {configured_probes}")

    # configure writers
    config_writers = set(config.get("writers", {}).keys())
    available_writers = {p.__name__ for p in writers}
    available_writers_lower = {p.__name__.lower() for p in writers}
    unknown_writers = {
        w for w in config_writers if w.lower() not in available_writers_lower
    }
    if unknown_writers:
        logger.warning(
            f"Ignoring unknown writers from config: {sorted(unknown_writers)}"
        )
        logger.warning(f"Available writer names are: {sorted(available_writers)}")

    writers_map = {w.__name__.lower(): w for w in writers}
    config["writers"] = [
        writers_map[name.lower()](**writer)
        for name, writer in config.get("writers", {}).items()
        if name.lower() in writers_map
    ]
    configured_writers = sorted(w.__class__.__name__ for w in config["writers"])
    logger.info(f"Configured writers: {configured_writers}")

    config = {
        k: v
        for k, v in config.items()
        if k in ["frequency", "probes", "writers", "logging"]
    }

    return EngineConfig(**config)
