import os, json
import redis

def get_redis():
    endpoint = os.environ["REDIS_ENDPOINT"]  # host:port
    host, port = endpoint.split(":")
    return redis.Redis(host=host, port=int(port), decode_responses=True)

def cache_get_json(r, key):
    val = r.get(key)
    return json.loads(val) if val else None

def cache_set_json(r, key, obj, ttl_seconds: int):
    r.setex(key, ttl_seconds, json.dumps(obj))

