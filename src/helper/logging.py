import json
import logging
import logging.config
from datetime import date, datetime, timezone
from typing import Any
from uuid import UUID

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    static_fields: dict[str, Any] = {}

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = (
            log_record.get("timestamp") or datetime.now(timezone.utc).isoformat()
        )
        log_record["level"] = str(log_record.get("level") or record.levelname).upper()

        # Add standard fields
        log_record.update(
            {
                "process_name": record.processName,
                "process_id": record.process,
                "thread_name": record.threadName,
                "thread_id": record.thread,
                "logger_name": record.name,
                "pathname": record.pathname,
                "line": record.lineno,
                "message": record.message,
            }
        )

        # Add extra_info if present
        extra_info = getattr(record, "extra_info", {})
        log_record["req"] = extra_info.get("req")
        log_record["res"] = extra_info.get("res")

        log_record.update(self.static_fields)


class DockerJsonFormatter(CustomJsonFormatter):
    def __init__(self, *_args: Any, **kwargs: Any):
        super().__init__("%(timestamp) %(level) %(name) %(message)", **kwargs)  # type: ignore


class ApacheFormatter(logging.Formatter):
    def __init__(self, *_args: Any, **_kwargs: Any):
        super().__init__(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt=None,
            style="%",
        )


class RichTextFormatter(DockerJsonFormatter):
    def __init__(self, *_args, **kwargs) -> None:  # type: ignore
        self.fields_separator: str = kwargs.pop("fieldsSeparator", " - ")
        super().__init__(**kwargs)

    def format(self, record: logging.LogRecord) -> str:
        s = super().format(record)
        data = json.loads(s)
        kvl = [f"{key}: {value}" for key, value in data.items()]
        return self.fields_separator.join(kvl)


class CustomJSONEncoder(json.JSONEncoder):
    """Custom Json Encode that also handle special types"""

    @staticmethod
    def _encode(obj: Any) -> Any:
        if isinstance(obj, dict):

            def transform_type(o: Any) -> Any:
                if isinstance(o, datetime):
                    return o.strftime("%Y-%m-%dT%H:%M:%SZ")
                if isinstance(o, date):
                    return o.strftime("%Y-%m-%d")
                if isinstance(o, UUID):
                    return str(o)
                if isinstance(o, set):
                    return list(o)

                return o

            return {transform_type(k): transform_type(v) for k, v in obj.items()}

        return obj

    def encode(self, obj: Any) -> str:
        return super().encode(self._encode(obj))

    def default(self, o: Any) -> Any:
        if isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%dT%H:%M:%SZ")
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, set):
            return list(o)

        return json.JSONEncoder.default(self, o)


def init_loggers(config: dict[str, Any]) -> None:
    """Initialize loggers"""
    if "logging" in config:
        logging.config.dictConfig(config["logging"])
    else:
        logging.config.dictConfig(config)
