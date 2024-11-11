import argparse
import socket

from models import Request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("-p", "--port", type=int, default=80)
    args = parser.parse_args()

    client_sock = socket.socket()
    client_sock.connect((args.host, args.port))

    request = Request("GET", args.host)
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
