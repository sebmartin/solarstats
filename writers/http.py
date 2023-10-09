import logging
from typing import Any, Optional
from writers import MetricsWriter
from prometheus_client import start_http_server, Gauge

logger = logging.getLogger(__name__)


class Http(MetricsWriter):
    def __init__(self, port: int = 5000, keys: Optional[list[str]] = None) -> None:
        super().__init__()

        self.port = port
        self.keys = keys
        self.__started = False
        self.__gauges: dict[str, Gauge] = {}

    def __start(self, keys: list[str]):
        if self.__started:
            return

        logger.info(f"Starting http server at: http://localhost:{self.port}")
        start_http_server(port=self.port)
        self.__started = True

    def output_metrics(self, provider: str, version: str, data: dict[str, Any]):
        keys = self.keys or list(data.keys())

        ignored_keys = [
            key for key in keys if not isinstance(data.get(key), (float, int))
        ]
        if ignored_keys:
            logger.debug(f"Ignoring non-float metrics: {ignored_keys}")

        for key in sorted(set(keys) - set(ignored_keys)):
            metric_value = data.get(key)
            if not metric_value:
                continue

            gauge = self.__gauges.get(key)
            if not gauge:
                name = key.replace("_", " ").title()
                gauge = Gauge(key, name)
                self.__gauges[key] = gauge
            gauge.set(metric_value)

        self.__start(keys)
