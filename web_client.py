import argparse
import socket


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("-p", "--port", type=int, default=80)
    args = parser.parse_args()

    client_sock = socket.socket()
    client_sock.connect((args.host, args.port))

    # fmt: off
    header = (
        "GET / HTTP/1.1\r\n"
        f"Host: {args.host}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    # fmt: on
    request = header.encode("ISO-8859-1")
    client_sock.sendall(request)

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
