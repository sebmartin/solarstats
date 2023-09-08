from typing import Optional
from writers import MetricsWriter
from prometheus_client import start_http_server, Gauge


class HttpMetricsWriter(MetricsWriter):
    def __init__(self, port: int = 5000, keys: Optional[list[str]] = None) -> None:
        super().__init__()

        self.port = port
        self.keys = keys
        self.__started = False
        self.__gauges: dict[str, Gauge] = {}

    def __start(self, keys: list[str]):
        if self.__started:
            return

        start_http_server(port=self.port)
        self.__started = True

    def output_metrics(self, name: str, value: dict):
        keys = self.keys or list(value.keys())

        for key in keys:
            metric_value = value.get(key)
            if not metric_value:
                continue

            gauge = self.__gauges.get(key)
            if not gauge:
                name = key.replace("_", " ").title()
                gauge = Gauge(key, name)
                self.__gauges[key] = gauge
            gauge.set(metric_value)

        self.__start(keys)
