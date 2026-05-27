import json
import logging
from typing import Any

import redis.asyncio as aioredis
from redis import RedisError

logger = logging.getLogger("app.redis")


async def cache_get(redis: aioredis.Redis, key: str) -> Any | None:
    try:
        value = await redis.get(key)
        if value is None:
            return None
        return json.loads(value)
    except RedisError as e:
        logger.warning("cache_get failed key=%s: %s", key, e)
        return None


async def cache_set(redis: aioredis.Redis, key: str, value: Any, ttl: int) -> None:
    try:
        await redis.set(key, json.dumps(value), ex=ttl)
    except RedisError as e:
        logger.warning("cache_set failed key=%s: %s", key, e)


async def cache_delete(redis: aioredis.Redis, key: str) -> None:
    try:
        await redis.delete(key)
    except RedisError as e:
        logger.warning("cache_delete failed key=%s: %s", key, e)
