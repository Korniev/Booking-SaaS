from __future__ import annotations

import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.core.logging_context import timings_var


def _now_ms() -> float:
    return time.perf_counter() * 1000


@asynccontextmanager
async def span(name: str, meta: dict | None = None) -> AsyncIterator[None]:
    start = _now_ms()
    try:
        yield
    finally:
        end = _now_ms()
        timings = timings_var.get()
        timings.append(
            {
                "name": name,
                "ms": round(end - start, 2),
                "meta": meta or {},
            }
        )
        timings_var.set(timings)