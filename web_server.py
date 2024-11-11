import argparse
import socket
from typing import Any

from models import Response

HEADER_DELIMITER = b"\r\n\r\n"


def handle_connection(
    new_sock: socket.socket,
    client_addr: Any,
) -> None:
    request_buf = b""
    while True:
        data = new_sock.recv(4096)
        if not data:
            break
        request_buf += data
        if request_buf.find(HEADER_DELIMITER) != -1:
            # TODO: Handle payloads in the request
            break

    if request_buf:
        decoded_request = request_buf.decode("ISO-8859-1")
        request_line, *header_fields = decoded_request.split("\r\n")
        print(client_addr, request_line)

        response = Response(status_code=200, content="Hello!")
        new_sock.sendall(response.to_bytes())

    new_sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=28333)
    args = parser.parse_args()

    server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind(("", args.port))
    server_sock.listen()
    print(f"Server listening on port {args.port}...")

    try:
        while True:
            new_sock, client_addr = server_sock.accept()
            handle_connection(new_sock, client_addr)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, shutting down")
    finally:
        server_sock.close()


if __name__ == "__main__":
    main()
