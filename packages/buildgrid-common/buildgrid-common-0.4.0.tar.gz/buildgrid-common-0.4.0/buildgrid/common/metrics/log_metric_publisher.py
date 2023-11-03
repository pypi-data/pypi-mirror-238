import logging
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Iterator

from .metric_publisher import MetricPublisher

LOGGER = logging.getLogger(__name__)


class LogMetricPublisher(MetricPublisher):
    def __init__(self, prefix: str | None = None, level: int = logging.INFO):
        super().__init__(prefix)
        self._level = level

    def count(self, metric_name: str, count: int) -> None:
        LOGGER.log(self._level, "%s=%s", self._with_prefix(metric_name), count)

    def duration(self, metric_name: str, duration: timedelta) -> None:
        LOGGER.log(self._level, "%s.time=%.3fms", self._with_prefix(metric_name), duration.total_seconds() * 1000)

    @contextmanager
    def timeit(self, metric_name: str) -> Iterator[None]:
        start = datetime.now()
        try:
            yield
        finally:
            end = datetime.now()
            diff = end - start
            self.duration(metric_name, diff)

    def _with_prefix(self, metric_name: str) -> str:
        if not self._prefix:
            return metric_name
        else:
            return f"{self._prefix}.{metric_name}"
