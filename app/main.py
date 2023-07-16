# Uncomment this to pass the first stage
import socket
import asyncio


PORT = 6379
HOST = "localhost"

async def main():
    print("Logs from your program will appear here!")

    # use asyncio to start a socket server
    # # then call an async function to return PONG
    server = await asyncio.start_server(
        handler, HOST, PORT, limit=4096, reuse_port=True
    )

    async with server:
        await server.serve_forever()

def parse(input: str):
    DATA_TYPES = dict(
        SIMPLE_STRING="+",
        ERROR="-",
        INTEGER=":",
        BULK_STRING="$",
        ARRAY="*"
    )

    command, message = None, None
    if not input or input[0] not in DATA_TYPES.values():
        return command, message

    # tokens = input.replace("\\r\\n", "\r\n").split("\r\n")
    tokens = input.split()
    # print("TOKENS: ", tokens)

    numberOfMessage = tokens[0][1]
    # print('numOfMessage', numberOfMessage)

    command = tokens[2]
    messages = tokens[4:]

    return {
        "command": command,
        "tokens": tokens,
        "message": message
    }

STORAGE = {}
def setCommand(command, tokens):
    print('setcommand', command, tokens)




# this handler needs the while loop to keep opening for requests
async def handler(reader, writer):
    while True:
        print("new connection accepted!")
        data = await reader.read(100)
        # checks data stream so server doesn't crash and wait for data finish sending
        if not data:
            break

        req = parse(bytes(data).decode())
        command = req.get('command')
        tokens = req['tokens']
        message = req['message']
        print(command, tokens, message)

        if not command or not message or command.lower() == "ping":
            writer.write(bytes("+PONG\r\n", "utf-8"))

        elif command.lower() == "echo":
            writer.write(bytes("+" + message[1], encoding="utf-8"))

        elif command.lower() == "set":
            setCommand(**req)


if __name__ == "__main__":
    asyncio.run(main())
