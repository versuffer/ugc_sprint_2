import datetime as dt
import json
import logging
import os
from typing import Optional

from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError


class JSONFormatter(logging.Formatter):
    LOG_RECORD_BUILTIN_ATTRS = {
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
        "taskName",
    }

    CONTAINER = os.getenv('CONTAINER') or 'UNKNOWN_CONTAINER'
    NAMESPACE = os.getenv('NAMESPACE') or 'UNKNOWN_NAMESPACE'
    GIT_TAG = os.getenv('TAG') or 'UNKNOWN_TAG'

    IMMUTABLE_ATTRS = {
        "container",
        "namespace",
        "git_tag",
        "request_id",
    }

    def __init__(
        self,
        *,
        fmt_keys: Optional[dict[str, str]] = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        default_log_fields = {
            "container": self.CONTAINER,
            "namespace": self.NAMESPACE,
            "git_tag": self.GIT_TAG,
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(record.created, tz=dt.timezone.utc).isoformat(),
        }
        if record.exc_info is not None:
            default_log_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            default_log_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_val if (msg_val := default_log_fields.pop(val, None)) is not None else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(default_log_fields)

        for key, val in record.__dict__.items():
            if key not in self.LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        if (args := record.__dict__['args']) and isinstance(args, dict):
            for key, val in args.items():
                if key not in self.IMMUTABLE_ATTRS:
                    message[key] = val

        return message


class RequestIdHandlerMixin:
    def emit(self, record: logging.LogRecord):
        try:
            request_id = context.get('request_id') or 'NO_REQUEST_ID'
            record.__dict__['request_id'] = request_id
        except ContextDoesNotExistError:
            pass

        super().emit(record)  # type: ignore


class RequestIdStreamHandler(RequestIdHandlerMixin, logging.StreamHandler):
    pass
