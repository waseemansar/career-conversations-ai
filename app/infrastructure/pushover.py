import requests
from loguru import logger

from app.config.settings import settings

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"


def push(message: str) -> None:
    try:
        response = requests.post(
            PUSHOVER_URL,
            data={
                "token": settings.pushover_token,
                "user": settings.pushover_user,
                "message": message,
            },
            timeout=5,
        )

        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Pushover request timed out")
    except requests.exceptions.RequestException as e:
        logger.error(f"Pushover request failed: {e}")
