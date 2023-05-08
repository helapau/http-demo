import asyncio

async def tcp_client(message: str):
    # establish a network connection over TCP socket
    # TCP socket = IP address + port
    reader, writer = await asyncio.open_connection(
        'localhost', 9999)

    writer.write(message.encode())
    await writer.drain()
    print('client sent data')

    response = await reader.readline()
    response_text = response.decode()

    writer.close()
    await writer.wait_closed()
    print('Client closed connection')
    return response_text


async def main():
    print("Welcome to the text to uppercase service!")
    message = input("Please type in your message: ")
    # input() strips the trailing new line - add it back to the end
    message += "\n"
    result = await tcp_client(message)
    print(f"The result is: {result}")


if __name__ == "__main__":
    asyncio.run(main())