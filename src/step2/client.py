import asyncio

async def main():
    reader, writer = await asyncio.open_connection(
        "hela-httpbin.fly.dev", 80)

    # why does there need to be \r\n at the very end?
    request = "GET /get HTTP/1.0\r\nHost: hela-httpbin.fly.dev\r\n\r\n"

    writer.write(request.encode())
    await writer.drain()

    async for line in reader:
        print(line.decode())

    writer.close()
    await writer.wait_closed()
    print('Client closed connection')

if __name__ == "__main__":
    asyncio.run(main())


