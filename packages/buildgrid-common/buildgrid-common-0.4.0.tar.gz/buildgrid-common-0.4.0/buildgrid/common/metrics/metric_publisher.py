from abc import ABC, abstractmethod
from contextlib import contextmanager
from datetime import timedelta
from typing import ContextManager, Iterator

ERROR_SUFFIX = ".error"


class MetricPublisher(ABC):
    """A minimal interface to publish metrics"""

    def __init__(self, prefix: str | None = None):
        self._prefix = prefix

    @abstractmethod
    def count(self, metric_name: str, count: int) -> None:
        """Send a count metric

        Example:
            def some_func():
                metric_publisher.count("some_func", 1)
                # ...

        Args:
            metric_name (str): Name of the metric
            count (int): Count to increase
        """
        pass

    @abstractmethod
    def duration(self, metric_name: str, duration: timedelta) -> None:
        """Send a duration metric

        Example:
            def some_func():
                start = datetime.now()
                # ...
                end = datetime.now()
                metric_publisher.duration("some_func", end - start)
        Args:
            metric_name (str): Name of the metric
            duration (timedelta): Duration to publish
        """
        pass

    @abstractmethod
    def timeit(self, metric_name: str) -> ContextManager[None]:
        """Context manager to time a code block

        Example:
            def some_func():
                with metric_publisher.timeit("some_func"):
                    #...
                # a duration metric is published
        Args:
            metric_name (str): Name of the metric

        Returns:
            ContextManager[None]:
        """
        pass

    @contextmanager
    def common_metrics(self, metric_name: str) -> Iterator[None]:
        """Context manger that publishes metrics of one count, duration,
            and error count if an exception happens

        Args:
            metric_name (str): Name of the metric

        Yields:
            Iterator[None]:
        """
        self.count(metric_name, 1)
        try:
            with self.timeit(metric_name):
                yield
        except Exception:
            self.count(metric_name + ERROR_SUFFIX, 1)
            raise
