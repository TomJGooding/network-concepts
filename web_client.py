import argparse
import socket

from models import Request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-p", "--port", type=int, default=80)
    args = parser.parse_args()

    request = Request("GET", args.url)

    client_sock = socket.socket()
    client_sock.connect((request.url.host, args.port))

    client_sock.sendall(request.to_bytes())

    chunks = []
    while True:
        data = client_sock.recv(4096)
        if not data:
            break
        chunks.append(data)

    response = b"".join(chunks).decode("ISO-8859-1")
    print(response)

    client_sock.close()


if __name__ == "__main__":
    main()
