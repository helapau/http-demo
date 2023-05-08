import asyncio

async def handler(reader, writer):
    received = await reader.readline()
    message = received.decode()
    addr = writer.get_extra_info('peername')

    response = message.upper()
    print(response.encode('ascii'))
    writer.write(response.encode())
    await writer.drain()

    # why does server need to close the connection?
    writer.close()
    await writer.wait_closed()
    print(f"Server closed the connection from {addr}")

async def main():
    server = await asyncio.start_server(handler, 'localhost', 9999)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())