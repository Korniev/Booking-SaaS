from __future__ import annotations

import logging
import sys
from typing import Any

from pythonjsonlogger import json

from app.core.logging_context import request_id_var


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


class PayloadJsonFormatter(json.JsonFormatter):
    """
    Adds `payload` dict (if present) as structured JSON fields,
    not as a JSON string inside `message`.
    """

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)

        payload = getattr(record, "payload", None)
        if isinstance(payload, dict):
            log_record.update(payload)
            log_record.pop("payload", None)


def configure_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    root.setLevel(level)

    root.handlers = []

    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(RequestIdFilter())

    formatter = PayloadJsonFormatter("%(asctime)s %(levelname)s %(name)s %(request_id)s")
    handler.setFormatter(formatter)

    root.addHandler(handler)

    logging.getLogger("uvicorn.access").setLevel("WARNING")