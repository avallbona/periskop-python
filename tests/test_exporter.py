import json
import pytest

from periskop.exporter import ExceptionExporter
from .conftest import get_exception_with_context


@pytest.fixture
def exporter(collector):
    return ExceptionExporter(collector)


def test_export(collector, exporter, sample_http_context):
    expected = """
{
  "aggregated_errors": [
    {
      "aggregation_key": "Exception@a9a59d26",
      "total_count": 1,
      "severity": "error",
      "latest_errors": [
        {
          "error": {
            "class": "Exception",
            "message": "test",
            "stacktrace": ["NoneType: None"],
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
    exception_with_context = get_exception_with_context(collector)
    exception_with_context.uuid = "5d9893c6-51d6-11ea-8aad-f894c260afe5"
    exception_with_context.timestamp = "2020-02-17T22:42:45Z"
    exported = exporter.export()
    print(json.loads(exported))
    assert json.loads(exported) == json.loads(expected)
