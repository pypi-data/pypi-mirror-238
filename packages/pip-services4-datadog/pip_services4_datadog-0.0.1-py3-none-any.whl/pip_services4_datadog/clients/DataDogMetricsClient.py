# -*- coding: utf-8 -*-
import datetime
from typing import Optional, List, Any

from pip_services4_commons.convert import StringConverter
from pip_services4_commons.errors import ConfigException
from pip_services4_components.config import ConfigParams
from pip_services4_components.context import IContext, ContextResolver
from pip_services4_components.refer import IReferences
from pip_services4_config.auth import CredentialResolver
from pip_services4_http.clients import RestClient

from .DataDogMetric import DataDogMetric
from .DataDogMetricPoint import DataDogMetricPoint


class DataDogMetricsClient(RestClient):
    __default_config: ConfigParams = ConfigParams.from_tuples(
        "connection.protocol", "https",
        "connection.host", "api.datadoghq.eu",
        "connection.port", 443,
        "credential.internal_network", "true"
    )

    def __init__(self, config: ConfigParams = None):
        super().__init__()

        self.__credential_resolver: CredentialResolver = CredentialResolver()

        if config:
            self.configure(config)

        self._base_route = 'api/v1'

    def configure(self, config: ConfigParams):
        config = self.__default_config.override(config)
        super().configure(config)
        self.__credential_resolver.configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self.__credential_resolver.set_references(references)

    def open(self, context: Optional[str]):
        credential = self.__credential_resolver.lookup(context)

        if credential is None or credential.get_access_key() is None:
            raise ConfigException(
                ContextResolver.get_trace_id(context),
                "NO_ACCESS_KEY",
                "Missing access key in credentials"
            )

        self._headers = self._headers or {}
        self._headers['DD-API-KEY'] = credential.get_access_key()

        super().open(context)

    def __convert_tags(self, tags: dict) -> Optional[str]:
        if tags is None:
            return

        builder = ''

        for key in tags:
            if builder != '':
                builder += ','
            builder += key + ':' + tags[key]

        return builder

    def __convert_points(self, points: List[DataDogMetricPoint]) -> List[List[str]]:
        results = []
        for point in points:
            time = point.time or datetime.datetime.now()
            results.append([
                str(time.timestamp()),
                StringConverter.to_string(point.value)
            ])

        return results

    def __convert_metric(self, metric: DataDogMetric) -> dict:
        tags = metric.tags

        if metric.service:
            tags = tags or {}
            tags['service'] = metric.service

        result = {
            'metric': metric.metric,
            'type': metric.type or 'gauge',
            'points': self.__convert_points(metric.points)
        }

        if tags:
            result['tags'] = self.__convert_tags(tags)
        if metric.tags:
            result['host'] = metric.host
        if metric.interval:
            result['interval'] = metric.interval

        return result

    def __convert_metrics(self, metrics: List[DataDogMetric]) -> dict:
        series = list(map(lambda m: self.__convert_metric(m), metrics))

        return {
            'series': series
        }

    def send_metrics(self, context: Optional[IContext], metrics: List[DataDogMetric]) -> Any:
        data = self.__convert_metrics(metrics)
        # Commented instrumentation because otherwise it will never stop sending logs...
        # timing = self._instrument(context, 'datadog.send_metrics')
        try:
            return self._call('post', 'series', None, None, data)
        finally:
            # timing.end_timing()
            pass
