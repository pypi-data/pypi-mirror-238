from contextlib import contextmanager
from datetime import timedelta
from typing import Iterator

from statsd import StatsClient

from .metric_publisher import MetricPublisher


class StatsdMetricPublisher(MetricPublisher):
    def __init__(self, statsd_client: StatsClient, prefix: str | None = None):
        super().__init__(prefix)
        self._client = statsd_client

    @classmethod
    def new(cls, host: str, port: int, prefix: str | None = None) -> "StatsdMetricPublisher":
        statsd_client = StatsClient(host=host, port=port, prefix=prefix)
        return cls(statsd_client, prefix)

    def count(self, metric_name: str, count: int) -> None:
        self._client.incr(metric_name, count)

    def duration(self, metric_name: str, duration: timedelta) -> None:
        self._client.timing(metric_name, duration)

    @contextmanager
    def timeit(self, metric_name: str) -> Iterator[None]:
        with self._client.timer(metric_name):
            yield
