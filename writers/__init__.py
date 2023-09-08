from abc import ABC, abstractmethod
from typing import Any


class MetricsWriter(ABC):
    @abstractmethod
    def output_metrics(self, provider: str, data: dict[str, Any]):
        raise NotImplementedError()
