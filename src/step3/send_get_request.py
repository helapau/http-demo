import asyncio
import urllib.parse


async def send_get(url):
    url = urllib.parse.urlsplit(url)
    if url.scheme == 'https':
        reader, writer = await asyncio.open_connection(
            url.hostname, 443, ssl=True)
    else:
        reader, writer = await asyncio.open_connection(
            url.hostname, 80)

    request = (
        f"GET {url.path or '/'}{'?' + url.query or ''} HTTP/1.0\r\n" # request line
        f"Host: {url.hostname}\r\n" # headers
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
    http://paulgraham.com
    """
    asyncio.run(send_get(url))


