# Uncomment this to pass the first stage
import socket
from concurrent.futures import ThreadPoolExecutor

def reply(c):
    while True:
        if not c.recv(1024):
            break
        c.send(bytes("+PONG\r\n", "utf-8"))
    print("Client disconnected")

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    threadPoolExecutor = ThreadPoolExecutor(max_workers=3)
    while True:
        c, _ = server_socket.accept()
        threadPoolExecutor.submit(reply, c)


if __name__ == "__main__":
    main()
