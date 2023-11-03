import json

from .interaction import interaction


def serverless_handler(event, context):
    if event['httpMethod'] == "POST":
        raw_request = json.loads(event.body)
        print(f"👉 Request: {raw_request}")
        return {"statusCode": "200",
                "body": interaction.interact(raw_request),
                "headers": {"Content-Type": "application/json"}}
