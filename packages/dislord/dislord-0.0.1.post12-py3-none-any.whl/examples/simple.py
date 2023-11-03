from dotenv import load_dotenv

from dislord import interaction, server

load_dotenv()


@interaction.command(name="hello")
def hello():
    return "hello world"


if __name__ == '__main__':
    server.start_server()
