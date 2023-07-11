import asyncio
import urllib.parse

from message_parsing import parse_status_line, parse_headers, parse_body
from utils import is_empty, CRLF, print_headers


class Connection:
    def __init__(self, reader, writer, protocol, hostname, port):
        self.reader = reader
        self.writer = writer
        self.protocol = protocol
        self.hostname = hostname
        self.port = port

        self.closed = False
        self.reason_closed = None

    def can_use(self, other_url) -> bool:
        url = urllib.parse.urlsplit(other_url)
        return all([
            url.scheme == self.protocol,
            url.hostname == self.hostname,
            url.port == self.port
        ])

    async def close(self, reason) -> None:
        self.reason_closed = reason
        self.closed = True
        self.writer.close()
        await self.writer.wait_closed()

    @staticmethod
    def should_close(first_line, headers) -> tuple:
        if b"1.0" in first_line.http_version and b"connection" not in headers:
            return True, "Server uses HTTP/1.0 and Connection header is missing"
        if b"close" in headers[b"connection"]:
            return True, "`Connection: close` in headers"
        return False, ""

    async def send_request(self, url) -> tuple:
        url = urllib.parse.urlsplit(url)
        query = "" if is_empty(url.query) else "?" + url.query
        request = (
            f"GET {url.path or '/'}{query} HTTP/1.1\r\n" # request line
            f"Host: {url.netloc}\r\n" # host is the only mandatory header in HTTP/1.1
            f"Connection: keep-alive\r\n"
            "\r\n" # there is no body - this is the end
        )
        self.writer.write(request.encode())
        # read until CRLF to ge the first-line (e.g. status line)
        # continue reading until CRLF -> you may get headers
        # what headers indicate the presence of response body? -> content-length or transfer-encoding
        raw_first_line = await self.reader.readuntil(CRLF)
        first_line = parse_status_line(raw_first_line)
        print(first_line, "\n")
        headers = await parse_headers(self.reader)
        print_headers(headers)
        body = await parse_body(self.reader, headers)
        print(body) if body is not None else None
        return first_line, headers

class Client:
    def __init__(self):
        self._connection: Connection = None

    async def _open_connection(self, url):
        url = urllib.parse.urlsplit(url)
        if url.scheme == 'https':
            port = 443 if is_empty(url.port) else url.port
            reader, writer = await asyncio.open_connection(
                url.hostname, port, ssl=True)
        else:
            port = 80 if is_empty(url.port) else url.port
            reader, writer = await asyncio.open_connection(
                url.hostname, port)
        self._connection = Connection(reader, writer, url.scheme, url.hostname, url.port)
        print("Opened new connection")

    async def _close_connection(self, reason):
        await self._connection.close(reason)
        self._connection = None
        print("Closed connection")

    async def get(self, url):
        if self._connection is None or not self._connection.can_use(url):
            await self._open_connection(url)

        first_line, headers = await self._connection.send_request(url)
        should_close, reason = Connection.should_close(first_line, headers)
        if should_close:
            await self._close_connection(reason)


async def main():
    """
    https://hela-httpbin.fly.dev/post
    http://hela-httpbin.fly.dev/status/404
    http://anglesharp.azurewebsites.net/Chunked
    https://www.httpwatch.com/httpgallery/chunked/chunkedimage.aspx
    """

    requests_same_server = [
        "http://hela-httpbin.fly.dev/image/svg",
        "http://hela-httpbin.fly.dev/get?howareyou=good",
        "http://hela-httpbin.fly.dev/stream-bytes/100", # chunked encoding
        "http://hela-httpbin.fly.dev/post"
    ]

    # should fail
    requests_different_server = [
        "http://libsql.org/hrana-client-ts/",
        "http://hela-httpbin.fly.dev/headers"
    ]

    client = Client()

    image = ["http://hela-httpbin.fly.dev/image/jpeg"]

    for r in requests_same_server:
        await client.get(r)



if __name__ == "__main__":
    asyncio.run(main())


