from flask import Flask, request

from .interaction import interaction

app = Flask(__name__)


@app.route("/", methods=["POST"])
async def interactions_endpoint():
    raw_request = request.json
    print(f"👉 Request: {raw_request}")
    return interaction.interact(raw_request)


def start_server():
    app.run(host='0.0.0.0', debug=True, port=8123, threaded=True)
