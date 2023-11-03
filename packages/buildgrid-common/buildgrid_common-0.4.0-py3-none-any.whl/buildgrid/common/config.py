# Copyright (C) 2023 Bloomberg LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
from enum import Enum
from typing import Annotated, Literal

from grpc import ServerCredentials, ssl_server_credentials
from pydantic import BaseModel, Field

from buildgrid.common.metrics.log_metric_publisher import LogMetricPublisher
from buildgrid.common.metrics.metric_publisher import MetricPublisher
from buildgrid.common.metrics.statsd_metric_publisher import StatsdMetricPublisher


class MetricPublisherMode(str, Enum):
    LOG = "log"
    STATSD = "statsd"


class LogMetricPublisherConfig(BaseModel):
    mode: Literal["log"] = "log"
    name: str = "log_metric_publisher"
    level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"] = "INFO"
    prefix: str | None = "buildgrid.logstream"


class StatsdMetricPublisherConfig(BaseModel):
    mode: Literal["statsd"] = "statsd"
    name: str = "statsd_metric_publisher"
    prefix: str = "buildgrid.logstream"
    statsd_host: str = "localhost"
    statsd_port: int = 8125


MetricPublisherConfig = Annotated[LogMetricPublisherConfig | StatsdMetricPublisherConfig, Field(discriminator="mode")]


def create_metric_publisher(config: MetricPublisherConfig) -> MetricPublisher:
    if config.mode == MetricPublisherMode.LOG.value:
        return LogMetricPublisher(prefix=config.prefix, level=logging.getLevelName(config.level))
    elif config.mode == MetricPublisherMode.STATSD.value:
        return StatsdMetricPublisher.new(host=config.statsd_host, port=config.statsd_port, prefix=config.prefix)
    else:
        raise ValueError("Invalid metric publisher config")


class TLSCredentials(BaseModel):
    key_path: str
    """File path to TLS key in PEM format"""
    cert_path: str
    """File path to TLS certificate in PEM format"""


def create_server_credentials(config: TLSCredentials) -> ServerCredentials:
    with open(config.key_path, "rb") as f:
        key = f.read()
    with open(config.cert_path, "rb") as f:
        cert = f.read()
    return ssl_server_credentials([(key, cert)])
