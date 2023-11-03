import json

from .interaction import interaction


def serverless_handler(event, context):
    if event['httpMethod'] == "POST":
        print(f"🫱 Full Event: {event}")
        raw_request = json.loads(event["body"])
        print(f"👉 Request: {raw_request}")
        raw_headers = event["headers"]
        signature = raw_headers.get('x-signature-ed25519')
        timestamp = raw_headers.get('x-signature-timestamp')
        response = interaction.interact(raw_request, signature, timestamp).as_serverless_response()
        print(f"🫴 Response: {response}")
        return response
