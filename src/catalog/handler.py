import os
from common.responses import ok
from common.db import fetch_one, fetch_all
from common.cache import get_redis, cache_get_json, cache_set_json
from common.metrics import put_metric

TITLE_TTL = 300
HOME_TTL = 60

def handler(event, context):
    path = event.get("rawPath") or event.get("path") or ""
    params = (event.get("pathParameters") or {})
    r = get_redis()

    # GET /catalog/{titleId}
    title_id = params.get("titleId")
    if title_id:
        key = f"title:{title_id}"
        cached = cache_get_json(r, key)
        if cached:
            put_metric("CacheHit", 1)
            return ok({"source":"redis", **cached})

        put_metric("CacheMiss", 1)
        row = fetch_one("SELECT * FROM titles WHERE id=%s", (title_id,))
        if not row:
            return ok({"error":"not found"}, 404)
        cache_set_json(r, key, row, TITLE_TTL)
        return ok({"source":"db", **row})

    # GET /catalog (home feed)
    home_key = "catalog:home"
    cached = cache_get_json(r, home_key)
    if cached:
        put_metric("CacheHit", 1)
        return ok({"source":"redis", "items": cached})

    put_metric("CacheMiss", 1)
    rows = fetch_all("SELECT id,name,year,genre FROM titles ORDER BY year DESC LIMIT 50", ())
    cache_set_json(r, home_key, rows, HOME_TTL)
    return ok({"source":"db", "items": rows})
