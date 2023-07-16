# Uncomment this to pass the first stage
import socket
import asyncio
import time

PORT = 6379
HOST = "localhost"

async def main():
    print("==================로그 보는 곳==========================")

    # use asyncio to start a socket server
    # # then call an async function to return PONG
    server = await asyncio.start_server(
        handler, HOST, PORT, limit=4096, reuse_port=True
    )

    async with server:
        await server.serve_forever()

def odd_index_elements(lst):
    return [val for idx, val in enumerate(lst) if idx % 2 != 0]

def parse(input: str):
    DATA_TYPES = dict(
        SIMPLE_STRING="+",
        ERROR="-",
        INTEGER=":",
        BULK_STRING="$",
        ARRAY="*"
    )

    # command, message = None, None
    # if not input or input[0] not in DATA_TYPES.values():
    #     return command, message

    tokens = input.split()
    # numberOfMessage = tokens[0][1]

    command = tokens[2]
    messages = odd_index_elements(tokens[3:])

    return {
        "command": command,
        "tokens": tokens,
        "message": messages
    }

def currentTimeMillis():
    return int((time.time() * 1000))

STORAGE = {}
def setCommand(message):
    key = message[0]
    value = message[1]

    if 'px' in message:
        idx = message.index('px')
        # print(message[idx+1])
        STORAGE[key] = {'value': value, 
                        'expireTimestamp': currentTimeMillis() + int(message[idx+1])}
        # print('STORAGE', STORAGE)
    else:
        STORAGE[key] = {'value': value}



def getCommand(message):
    key = message[0]
    valueMap = STORAGE[key]
    print('valueMap', valueMap)

    expireTimestamp = valueMap.get('expireTimestamp', None)
    _currentTimeMillis = currentTimeMillis()
    print('cur=', _currentTimeMillis)
    print('exp=', expireTimestamp)
    # print('cur=' + currentTimeMillis + ',exp=' + expireTimestamp)

    if expireTimestamp is not None and _currentTimeMillis > expireTimestamp:
        return None

    return valueMap['value']


# this handler needs the while loop to keep opening for requests
async def handler(reader, writer):
    while True:
        # print("new connection accepted!")
        data = await reader.read(100)
        # checks data stream so server doesn't crash and wait for data finish sending
        if not data:
            break

        req = parse(bytes(data).decode())
        command = req.get('command')
        tokens = req['tokens']
        message = req['message']

        if not command or not message or command.lower() == "ping":
            writer.write(bytes("+PONG\r\n", "utf-8"))

        elif command.lower() == "echo":
            writer.write(bytes("+" + ''.join(message), encoding="utf-8"))

        elif command.lower() == "set":
            setCommand(message)
            writer.write(b"+OK\r\n")
        elif command.lower() == "get":
            v = getCommand(message)
            if v is not None:
                writer.write(bytes("+" + v + "\r\n", encoding="utf-8"))
            else:
                writer.write(bytes("$-1\r\n", "utf-8"))


if __name__ == "__main__":
    asyncio.run(main())
