import json
import os
from typing import Any, Optional
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))


def get_redis_client():
    try:
        client = redis.from_url(REDIS_URL, decode_responses=True)
        client.ping()
        return client
    except Exception:
        return None


def get_cache(key: str) -> Optional[Any]:
    client = get_redis_client()
    if not client:
        return None
    value = client.get(key)
    if value is None:
        return None
    return json.loads(value)


def set_cache(key: str, value: Any, ttl: int = CACHE_TTL_SECONDS) -> None:
    client = get_redis_client()
    if not client:
        return
    client.setex(key, ttl, json.dumps(value, default=str))


def delete_cache_pattern(pattern: str) -> None:
    client = get_redis_client()
    if not client:
        return
    keys = client.keys(pattern)
    if keys:
        client.delete(*keys)
