import logging

import redis.asyncio as aioredis

logger = logging.getLogger("app.redis")

_redis: aioredis.Redis | None = None


async def init_redis(url: str) -> None:
    global _redis
    _redis = aioredis.from_url(url, encoding="utf-8", decode_responses=True)
    await _redis.ping()
    logger.info("Redis connected")


async def close_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None
        logger.info("Redis connection closed")


def get_redis() -> aioredis.Redis:
    if _redis is None:
        raise RuntimeError("Redis not initialized")
    return _redis
