import logging
import sys

from pythonjsonlogger import json

from app.core.config import settings


def configure_logging() -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)

    # avoid duplicates (e.g. reload)
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        json.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    root_logger.addHandler(handler)