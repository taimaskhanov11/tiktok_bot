import logging
import sys
from pathlib import Path

from loguru import logger as log

from tiktok_bot.config.config import LOG_DIR

LOG_DIR.mkdir(exist_ok=True)


def init_logging(filename="", old_logger=True, level="TRACE", old_level=logging.INFO, steaming=True, write=True):
    log.remove()
    if steaming:
        log.add(
            sink=sys.stdout,
            # colorize=True,
            level=level,
            enqueue=True,
            diagnose=True,
            # format="{time} - {level} - {message}"
        )
    if write:
        log.add(
            sink=Path(LOG_DIR, f"base{filename}.log"),
            level=level,
            enqueue=True,
            encoding="utf-8",
            diagnose=True,
            rotation="5MB",
            compression="zip",
        )
    if old_logger:
        handlers = []
        if steaming:
            handlers.append(logging.StreamHandler())
        if write:
            handlers.append(logging.FileHandler(filename=Path(LOG_DIR, f"default{filename}.log"), encoding="utf-8"))

        if handlers:
            logging.basicConfig(
                encoding="utf-8",
                level=old_level,
                format="{levelname} [{asctime}] {name}: {message}",
                style="{",
                handlers=handlers,
            )


if __name__ == "__main__":
    init_logging(old_logger=True, level="TRACE", old_level=logging.INFO, steaming=True, write=True)
    log.info("hi")
