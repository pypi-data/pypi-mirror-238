
from flask import jsonify
from discord_interactions import verify_key_decorator

from .env import DISCORD_PUBLIC_KEY

class Interaction:
    def __init__(self):
        self.commands = {}

    @verify_key_decorator(DISCORD_PUBLIC_KEY)
    def interact(self, raw_request):
        if raw_request["type"] == 1:  # PING
            response_data = {"type": 1}  # PONG
        else:
            data = raw_request["data"]
            command_name = data["name"]

            if command_name == "hello":
                message_content = self.commands[command_name]()
            elif command_name == "echo":
                original_message = data["options"][0]["value"]
                message_content = f"Echoing: {original_message}"

            response_data = {
                "type": 4,
                "data": {"content": message_content},
            }

        return jsonify(response_data)

    def command(self, *, name):
        def decorator(func):
            self.commands[name] = func
            return func

        return decorator

interaction = Interaction()
