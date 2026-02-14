from __future__ import annotations

import contextvars
from typing import Any

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")
timings_var: contextvars.ContextVar[list[dict[str, Any]] | None] = contextvars.ContextVar("timings", default=None)
