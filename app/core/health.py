from loguru import logger
from qdrant_client import QdrantClient
from upstash_redis import Redis

from app.config.settings import settings


def check_redis(redis: Redis) -> None:
    try:
        redis.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.critical(f"Redis ping failed on startup: {e}")
        raise RuntimeError("Redis is unreachable, shutting down") from e


def check_qdrant(client: QdrantClient) -> None:
    try:
        collections = client.get_collections().collections
        names = [c.name for c in collections]

        if settings.qdrant_collection_name not in names:
            logger.critical(
                f"Qdrant collection '{settings.qdrant_collection_name}' not found"
            )
            raise RuntimeError("Qdrant collection not found, shutting down")

        logger.info("Qdrant connection established")
    except RuntimeError:
        raise
    except Exception as e:
        logger.critical(f"Qdrant check failed on startup: {e}")
        raise RuntimeError("Qdrant is unreachable, shutting down") from e
