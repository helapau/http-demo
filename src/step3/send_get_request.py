import asyncio
import urllib.parse


async def send_get(url):
    def is_empty(p):
        is_none = p is None
        is_empty = False
        if type(p) is str:
            is_empty = len(p) == 0
        return is_none or is_empty

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

    async for line in reader:
        print(line.decode())

    writer.close()
    await writer.wait_closed()
    return


if __name__ == "__main__":
    url = input("Please type in the URL you want to visit: ")
    """
    https://hela-httpbin.fly.dev/get?some=parameter&and=another
    https://hela-httpbin.fly.dev/post
    http://hela-httpbin.fly.dev/status/404
    http://hela-httpbin.fly.dev/headers
    http://libsql.org/hrana-client-ts/
    https://demo.chystat.com:8443    
    """
    asyncio.run(send_get(url))




