class Request:
    def __init__(
        self,
        method: str,
        host: str,
    ) -> None:
        self.method = method
        self.host = host

    def to_bytes(self) -> bytes:
        header = (
            f"{self.method} / HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ISO-8859-1")
        return header


class Response:
    STATUS_MESSAGES = {
        200: "OK",
        404: "Not Found",
    }

    def __init__(
        self,
        status_code: int,
        content: str,
    ) -> None:
        if status_code not in self.STATUS_MESSAGES:
            raise ValueError(f"Invalid status code: {status_code}")

        self.status_code = status_code
        self.status_message = self.STATUS_MESSAGES[status_code]
        self.content = content
        self.content_type = "text/plain"

    def to_bytes(self) -> bytes:
        content = self.content.encode("ISO-8859-1")

        header = (
            f"HTTP/1.1 {self.status_code} {self.status_message}\r\n"
            f"Content-Type: {self.content_type}\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ISO-8859-1")

        response = header + content
        return response
