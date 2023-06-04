import asyncio
import urllib.parse

from response_parser import parse_status_line, parse_headers, parse_body
from utils import is_empty, CRLF


async def send_get(url):
    url = urllib.parse.urlsplit(url)
    if url.scheme == 'https':
        port = 443 if is_empty(url.port) else url.port
        reader, writer = await asyncio.open_connection(
            url.hostname, port, ssl=True)
    else:
        port = 80 if is_empty(url.port) else url.port
        reader, writer = await asyncio.open_connection(
            url.hostname, port)

    query = "" if is_empty(url.query) else "?" + url.query
    request = (
        f"GET {url.path or '/'}{query} HTTP/1.0\r\n" # request line
        f"Host: {url.netloc}\r\n" # headers
        "\r\n" # there is no body - this is the end
    )

    writer.write(request.encode())
    # read until CRLF to ge the first-line (e.g. status line)
    # continue reading until CRLF -> you may get headers
    # what headers indicate the presence of response body? -> content-length or transfer-encoding

    raw_first_line = await reader.readuntil(CRLF)
    first_line = parse_status_line(raw_first_line)
    headers = await parse_headers(reader)
    body = await parse_body(reader, headers)
    print(first_line, "\n")
    for k in headers:
        print(k.decode(), ": ", headers[k].decode())
    print("\n")
    print(body)

    writer.close()
    await writer.wait_closed()
    return


if __name__ == "__main__":
    # url = input("Please type in the URL you want to visit: ")
    """
    https://hela-httpbin.fly.dev/get?some=parameter&and=another
    https://hela-httpbin.fly.dev/post
    http://hela-httpbin.fly.dev/status/404
    http://hela-httpbin.fly.dev/headers
    http://libsql.org/hrana-client-ts/
    https://demo.chystat.com:8443
    http://hela-httpbin.fly.dev/image/jpeg
    http://hela-httpbin.fly.dev/cookies
    http://hela-httpbin.fly.dev/brotli    
    """
    url = "http://hela-httpbin.fly.dev/html"
    asyncio.run(send_get(url))





