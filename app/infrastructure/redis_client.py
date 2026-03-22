from upstash_redis import Redis

from app.config.settings import settings

redis = Redis(
    url=settings.upstash_redis_rest_url, token=settings.upstash_redis_rest_token
)
