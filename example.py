import json
from http.server import HTTPServer

from periskop.collector import ExceptionCollector
from periskop.exporter import ExceptionExporter
from periskop.handler import exception_http_handler
from periskop.types import HTTPContext


def faulty_json():
    return json.loads('{"id":')


if __name__ == "__main__":
    collector = ExceptionCollector()
    try:
        faulty_json()
    except Exception as exception:
        # Report without context
        collector.report(exception)
        # Report with HTTP context
        collector.report_with_context(exception,
                                      HTTPContext("GET", "http://example.com", {"Cache-Control": "no-cache"}))

    # Expose collected exceptions in localhost:8081/-/exceptions
    server_address = ('', 8081)
    handler = exception_http_handler(path="/-/exceptions", exporter=ExceptionExporter(collector))
    http_server = HTTPServer(server_address, handler)
    http_server.serve_forever()
