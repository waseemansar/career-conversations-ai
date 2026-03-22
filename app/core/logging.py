import sys

from loguru import logger

from app.config.settings import settings


def setup_logging():
    logger.remove()  # Remove the default logger

    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )
