from __future__ import annotations

import json
import logging
import time
import traceback
import uuid
from typing import Any, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging_context import request_id_var, timings_var

logger = logging.getLogger("app.http")

SENSITIVE_HEADERS = {"authorization", "cookie"}
SENSITIVE_FIELDS = {"password", "access_token", "refresh_token", "token", "secret"}

MAX_BODY_CHARS = 8000  # guardrail


def _safe_headers(headers: dict[str, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in headers.items():
        out[k] = "***" if k.lower() in SENSITIVE_HEADERS else v
    return out


def _mask_sensitive(obj: Any) -> Any:
    if isinstance(obj, dict):
        masked = {}
        for k, v in obj.items():
            if str(k).lower() in SENSITIVE_FIELDS:
                masked[k] = "***"
            else:
                masked[k] = _mask_sensitive(v)
        return masked
    if isinstance(obj, list):
        return [_mask_sensitive(x) for x in obj]
    return obj


def _safe_body(request: Request, raw_body: bytes) -> str:
    if not raw_body:
        return ""

    content_type = request.headers.get("content-type", "").lower()
    if "multipart/form-data" in content_type:
        return "<multipart omitted>"

    text = raw_body.decode("utf-8", errors="ignore")
    if len(text) > MAX_BODY_CHARS:
        text = text[:MAX_BODY_CHARS] + "...(truncated)"

    try:
        data = json.loads(text)
        data = _mask_sensitive(data)
        return json.dumps(data, ensure_ascii=False)
    except Exception:
        return text


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        rid = str(uuid.uuid4())
        request_id_var.set(rid)
        timings_var.set([])

        start = time.perf_counter()

        raw_body = b""
        try:
            raw_body = await request.body()
        except Exception:
            raw_body = b""

        async def receive():
            return {"type": "http.request", "body": raw_body}

        request._receive = receive  # noqa: SLF001

        response: Response | None = None
        exc_text: str | None = None
        tb_text: str | None = None

        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = rid
            return response

        except Exception as exc:
            exc_text = str(exc)
            tb_text = traceback.format_exc()
            raise

        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            timings = timings_var.get() or []

            payload = {
                "topic": "http_request",
                "request_id": rid,
                "duration_ms": duration_ms,
                "duration_s": round(duration_ms / 1000, 3),
                "request": {
                    "method": request.method,
                    "path": request.url.path,
                    "query": dict(request.query_params),
                    "headers": _safe_headers(dict(request.headers)),
                    "body": _safe_body(request, raw_body),
                },
                "response": {
                    "status_code": response.status_code if response else 500,
                    "exception": exc_text,
                    "traceback": tb_text,
                },
                "timings": timings,
            }

            logger.info("", extra={"payload": payload})