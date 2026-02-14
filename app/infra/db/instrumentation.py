from __future__ import annotations

import time
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.core.logging_context import timings_var


def _now_ms() -> float:
    return time.perf_counter() * 1000


def setup_sql_timing(engine: Engine) -> None:
    """
    Connect event listeners for calculate DB queries.
    Works for AsyncEngine with async_engine.sync_engine.
    """

    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        context._query_start_ms = _now_ms()

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        start = getattr(context, "_query_start_ms", None)
        if start is None:
            return

        ms = round(_now_ms() - start, 2)

        stmt = " ".join(statement.split())
        if len(stmt) > 400:
            stmt = stmt[:400] + "..."

        timings = timings_var.get()
        timings.append(
            {
                "name": "db.query",
                "ms": ms,
                "meta": {
                    "executemany": bool(executemany),
                    "sql": stmt,
                },
            }
        )
        timings_var.set(timings)