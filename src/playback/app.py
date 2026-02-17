import json
import os
import time
import boto3

sqs = boto3.client("sqs")
QUEUE_URL = os.environ.get("WATCH_EVENTS_QUEUE_URL", "")
CF_DOMAIN = os.environ.get("VIDEO_CLOUDFRONT_DOMAIN", "")

def _resp(status, body):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }

def handler(event, context):
    method = event.get("httpMethod", "")
    path_params = event.get("pathParameters") or {}

    if method == "GET" and "titleId" in path_params:
        title_id = path_params["titleId"]
        # TODO: Replace with real manifest signing / per-user entitlements
        manifest_url = f"https://{CF_DOMAIN}/hls/{title_id}/master.m3u8"
        return _resp(200, {"titleId": title_id, "manifestUrl": manifest_url})

    if method == "POST":
        body = event.get("body") or "{}"
        payload = json.loads(body)
        payload.setdefault("ts", int(time.time()))

        if not QUEUE_URL:
            return _resp(500, {"error": "WATCH_EVENTS_QUEUE_URL not set"})

        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(payload))
        return _resp(202, {"ok": True})

    return _resp(404, {"error": "not found"})

