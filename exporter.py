import uuid
from datetime import datetime


class ExceptionExporter:

    def _generate_error(self, error_class, message, stacktrace, severity=SEVERITY_ERROR):
        """

        :param list stacktrace:
        :param str severity:
        :return:
        """
        return {
            "error": {
                "class": error_class,
                "message": message,
                "stacktrace": stacktrace,
                "cause": None
            },
            "uuid": str(uuid.uuid1()),
            "timestamp": datetime.utcnow().isoformat(), #"2018-09-13T16:24:30.630Z",
            "severity": severity,
            "http_context": {
                "request_method": "GET",
                "request_url": "http://url",
                "request_headers": {
                    "Key": "value"
                }
            }
        }

