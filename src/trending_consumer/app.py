import json

def handler(event, context):
    # event["Records"] contains SQS messages
    for record in event.get("Records", []):
        msg = json.loads(record["body"])
        # TODO: Update trending counters in DB/Redis (or DynamoDB if you choose)
        print("Watch event:", msg)

    return {"ok": True}

