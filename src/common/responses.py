import json

def ok(body, status=200):
    return {"statusCode": status, "headers": {"content-type":"application/json"}, "body": json.dumps(body)}
