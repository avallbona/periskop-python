import hashlib
import uuid as _uuid
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from datetime import datetime
from typing import List, Dict, Optional

SEVERITY_INFO = "info"
SEVERITY_WARNING = "warning"
SEVERITY_ERROR = "error"
MAX_TRACES = 5
MAX_ERRORS = 10
NUM_HASH_CHARS = 8


@dataclass_json
@dataclass
class ExceptionInstance:
    cls: str = field(metadata=config(field_name="class"))
    message: str
    stacktrace: List[str]
    # should be ExceptionInstance, but we don't needed in this lib
    cause: object = None


@dataclass_json
@dataclass
class HTTPContext:
    request_method: str
    request_url: str
    request_headers: Dict[str, str]


@dataclass_json
@dataclass
class ExceptionWithContext:
    error: ExceptionInstance
    http_context: Optional[HTTPContext] = None
    severity: str = SEVERITY_ERROR
    uuid: str = str(_uuid.uuid1())
    timestamp: str = datetime.utcnow().isoformat()

    def _hash_exception(self, exception: str):
        h = hashlib.md5(exception.encode())
        return h.hexdigest()[:NUM_HASH_CHARS]

    def aggregation_key(self) -> str:
        """
        Generates the aggregation key with a hash using the last MAX_TRACES

        :return: str
        """
        stacktrace_head = self.error.stacktrace[:]
        if len(self.error.stacktrace) > MAX_TRACES:
            stacktrace_head = stacktrace_head[:MAX_TRACES]
        error_hash = self._hash_exception("".join(stacktrace_head))
        return f"{self.error.cls}@{error_hash}"


@dataclass_json
@dataclass
class AggregatedException:
    aggregation_key: str
    latest_errors: List[ExceptionWithContext]
    total_count: int = 0
    severity: str = SEVERITY_ERROR

    def add_exception(self, exception_with_context: ExceptionWithContext):
        """
        Add exception to the list of latest errors up to MAX_ERRORS

        :param ExceptionWithContext exception_with_context: exception with context that is being reported
        """
        if len(self.latest_errors) >= MAX_ERRORS:
            self.latest_errors.pop()
        self.latest_errors.append(exception_with_context)
        self.total_count += 1


@dataclass_json
@dataclass
class Payload:
    aggregated_errors: List[AggregatedException]
