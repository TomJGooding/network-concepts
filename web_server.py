import argparse
import socket


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=28333)
    args = parser.parse_args()

    server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind(("", args.port))
    server_sock.listen()
    print(f"Server listening on port {args.port}...")

    header_delimiter = b"\r\n\r\n"

    try:
        while True:
            new_sock, client_addr = server_sock.accept()
            print("New connection from", client_addr)

            request_buf = b""
            while True:
                data = new_sock.recv(4096)
                if not data:
                    break
                request_buf += data
                if request_buf.find(header_delimiter) != -1:
                    break

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 6\r\n"
                "Connection: close\r\n"
                "\r\n"
                "Hello!\r\n"
            ).encode("ISO-8859-1")

            new_sock.sendall(response)
            new_sock.close()

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, shutting down")
    finally:
        server_sock.close()


if __name__ == "__main__":
    main()
