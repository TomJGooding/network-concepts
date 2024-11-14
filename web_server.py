import argparse
import os
import socket
from typing import Any

from models import Request, Response

HEADER_DELIMITER = b"\r\n\r\n"


def handle_request(request: Request) -> Response:
    if request.method != "GET":
        return Response(
            status_code=405,
            content=b"405 Method Not Allowed",
            content_type="text/plain",
        )

    # Strip the path down to the filename for security
    # (Real web servers restrict the path to a certain directory)
    filename = os.path.split(request.url.path)[-1]

    file_extn = os.path.splitext(filename)[-1]
    if file_extn == ".html":
        content_type = "text/html"
    else:
        content_type = "text/plain"

    try:
        with open(filename, "rb") as fp:
            data = fp.read()
    except FileNotFoundError:
        return Response(
            status_code=404,
            content=b"404 Not Found",
            content_type="text/plain",
        )
    else:
        return Response(
            status_code=200,
            content=data,
            content_type=content_type,
        )


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
        request = parse_request(request_buf)

        response = handle_request(request)
        new_sock.sendall(response.to_bytes())

        print(
            client_addr,
            f'"{request.method} {request.url.path} HTTP/1.1"',
            response.status_code,
        )

    new_sock.close()


def parse_request(request_data: bytes) -> Request:
    request = request_data.decode("ISO-8859-1")
    request_line, *header_fields = request.split("\r\n")
    method, path, protocol = request_line.split()
    # TODO: Parse the request line properly!
    url = "localhost" + path

    return Request(method, url)


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
