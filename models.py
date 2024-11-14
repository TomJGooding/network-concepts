from typing import NamedTuple


class URL(NamedTuple):
    host: str
    path: str


class Request:
    def __init__(
        self,
        method: str,
        url: str,
    ) -> None:
        self.method = method
        self.url: URL = self._parse_url(url)

    def _parse_url(self, url: str) -> URL:
        # TODO: Handle URL schemes
        if "/" in url:
            host, path = url.split("/", maxsplit=1)
            path = "/" + path
        else:
            host = url
            path = "/"
        return URL(host, path)

    def to_bytes(self) -> bytes:
        header = (
            f"{self.method} {self.url.path} HTTP/1.1\r\n"
            f"Host: {self.url.host}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ISO-8859-1")
        return header


class Response:
    STATUS_MESSAGES = {
        200: "OK",
        404: "Not Found",
        405: "Method Not Allowed",
    }

    def __init__(
        self,
        status_code: int,
        content: bytes,
        content_type: str,
    ) -> None:
        if status_code not in self.STATUS_MESSAGES:
            raise ValueError(f"Invalid status code: {status_code}")

        self.status_code = status_code
        self.status_message = self.STATUS_MESSAGES[status_code]
        self.content = content
        self.content_type = content_type

    def to_bytes(self) -> bytes:
        header = (
            f"HTTP/1.1 {self.status_code} {self.status_message}\r\n"
            f"Content-Type: {self.content_type}\r\n"
            f"Content-Length: {len(self.content)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ISO-8859-1")

        response = header + self.content
        return response
