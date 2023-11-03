from dislord import interaction, server


@interaction.command(name="hello")
def hello():
    return "hello world"


if __name__ == '__main__':
    server.start_server()
