import json

from .interaction import interaction


def serverless_handler(event, context):
    if event['httpMethod'] == "POST":
        print(f"🫱 Full Event: {event}")
        raw_request = json.loads(event["body"])
        print(f"👉 Request: {raw_request}")
        raw_headers = json.loads(event["headers"])
        signature = raw_headers.get('X-Signature-Ed25519')
        timestamp = raw_headers.get('X-Signature-Timestamp')
        return interaction.interact(raw_request, signature, timestamp).as_serverless_response()
