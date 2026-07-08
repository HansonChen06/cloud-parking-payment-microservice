import logging

from pythonjsonlogger import json


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()
    formatter = json.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level.upper())
