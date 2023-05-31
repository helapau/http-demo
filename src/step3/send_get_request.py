import asyncio
import urllib.parse

from response_parser import parse_response
from utils import is_empty


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

    # todo: parse the response
    """
    extract: 
        - status
        - headers
    print: HTTP version, status code (int) + reason, headers
    """
    lines = []
    async for line in reader:
        lines.append(line.decode())

    response = parse_response(lines)
    print(response)

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
    """
    url = "http://hela-httpbin.fly.dev/patch"
    asyncio.run(send_get(url))





