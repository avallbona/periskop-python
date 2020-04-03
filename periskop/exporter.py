import dataclasses
import json

from .collector import ExceptionCollector


class ExceptionExporter:

    def __init__(self, collector: ExceptionCollector):
        self._collector = collector

    def export(self) -> str:
        """
        Export the collection of errors in JSON format

        :return: str
        """
        return json.dumps(dataclasses.asdict(self._collector.get_aggregated_exceptions()))
