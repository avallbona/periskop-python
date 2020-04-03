import json
import pytest
from freezegun import freeze_time

from periskop.exporter import ExceptionExporter


@pytest.fixture
def exporter(collector):
    return ExceptionExporter(collector)


@freeze_time("2020-02-17 22:42:45")
def test_export(collector, exporter, sample_http_context):
    expected = """
{
  "aggregated_errors": [
    {
      "aggregation_key": "test",
      "total_count": 1,
      "severity": "error",
      "latest_errors": [
        {
          "error": {
            "class": "Exception",
            "message": "test",
            "stacktrace": [],
            "cause": null
          },
          "uuid": "5d9893c6-51d6-11ea-8aad-f894c260afe5",
          "timestamp": "2020-02-17T22:42:45Z",
          "severity": "error",
          "http_context": {
            "request_method": "GET",
            "request_url": "http://example.com",
            "request_headers": {
              "Cache-Control": "no-cache"
            }
          }
        }
      ]
    }
  ]
}"""
    collector.report_with_context(exception=Exception("test"), http_context=sample_http_context)
    exported = exporter.export()
    assert json.loads(exported) == json.loads(expected)
