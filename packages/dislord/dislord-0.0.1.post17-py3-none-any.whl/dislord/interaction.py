import json

from flask import jsonify
from discord_interactions import verify_key

from .env import DISCORD_PUBLIC_KEY
from .types.api import HttpResponse, HttpUnauthorized, HttpOk


class Interaction:
    def __init__(self):
        self.commands = {}

    def interact(self, raw_request, signature, timestamp, client_public_key=DISCORD_PUBLIC_KEY) -> HttpResponse:
        if signature is None or timestamp is None or not verify_key(json.dumps(raw_request, separators=(',', ':'))
                                                                        .encode('utf-8'), signature, timestamp,
                                                                    client_public_key):
            return HttpUnauthorized('Bad request signature')

        if raw_request["type"] == 1:  # PING
            response_data = {"type": 1}  # PONG
        else:
            data = raw_request["data"]
            command_name = data["name"]

            message_content = self.commands[command_name]()

            if command_name == "echo":
                original_message = data["options"][0]["value"]
                message_content = f"Echoing: {original_message}"

            response_data = {
                "type": 4,
                "data": {"content": message_content},
            }

        return HttpOk(response_data, headers={"Content-Type": "application/json"})

    def command(self, *, name):
        def decorator(func):
            self.commands[name] = func
            return func

        return decorator

interaction = Interaction()
