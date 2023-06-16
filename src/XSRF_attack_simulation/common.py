from response_parser import convert_first_line_to_bytes


async def handle_not_found(writer):
    # create a 404 not found response
    # b"HTTP/1.0 404 NOT FOUND"
    status_line = convert_first_line_to_bytes(StatusLine(b'HTTP/1.0', b'404', b'NOT FOUND'))
    writer.write(status_line + b"\r\n") # one more \r\n because there is no body
    await writer.drain()
    return