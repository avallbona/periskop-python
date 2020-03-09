import hashlib
import traceback
from pprint import pprint


class ExceptionCollector:
    SEVERITY_ERROR = "error"

    def __init__(self):
        self.aggregated_errors = []

    def _hash_exception(self, exception):
        h = hashlib.md5(exception.encode())
        return h.hexdigest()[:8]

    def report(self, exception):
        """
        Report an exception

        :param exception:
        """
        self._add_exception(exception)

    def _add_exception(self, exception):
        #message = f"{type(exception).__name_}: {exception.args}"
        stacktrace = traceback.format_exc()
        error_hash = self._hash_exception(stacktrace)
        error_class = type(exception).__name__
        error_key = f"{error_class}@{error_hash}"
        error = self._generate_error(error_class, str(exception), stacktrace.splitlines())
        print(error_key)
        pprint(error)

