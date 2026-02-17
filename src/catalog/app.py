import json
import os

def _resp(status, body):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }

def handler(event, context):
    path = event.get("path", "")
    title_id = (event.get("pathParameters") or {}).get("titleId")

    # TODO: Replace with real DB + Redis lookups
    if title_id:
        return _resp(200, {"titleId": title_id, "name": "Example Title", "genres": ["drama"]})

    return _resp(200, {
        "items": [
            {"titleId": "t1", "name": "Example Title 1"},
            {"titleId": "t2", "name": "Example Title 2"},
        ],
        "note": "Stub response. Next: RDS schema + Redis hot catalog cache."
    })

