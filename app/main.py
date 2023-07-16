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
    print("TOKENS: ", tokens)

    numberOfMessage = tokens[0][1]
    print('numOfMessage', numberOfMessage)
    # 중요.
    # data_type = DATA_TYPES.get(tokens[0][0])
    

    for i in range(numberOfMessage):
        command_length = tokens[1][1:]  # $은 제거함.

    command = tokens[2]
    if len(tokens) > 4:
        message = tokens[4]

    return {
        "command": command,
        "tokens": tokens,
        "message": message
    }


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
            writer.write(bytes("+" + message, encoding="utf-8"))

if __name__ == "__main__":
    asyncio.run(main())
