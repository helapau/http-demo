import datetime as dt

from response_parser import convert_first_line_to_bytes, StatusLine, convert_headers_mapping_to_bytes
from step3.utils import CRLF


async def handle_not_found(writer):
    # create a 404 not found response
    # b"HTTP/1.0 404 NOT FOUND"
    status_line = convert_first_line_to_bytes(StatusLine(b'HTTP/1.0', b'404', b'NOT FOUND'))
    writer.write(status_line + CRLF) # one more \r\n because there is no body
    await writer.drain()
    return

async def handle_internal_server_error(writer, error_message):
    status_line = convert_first_line_to_bytes(StatusLine(b'HTTP/1.0', b'500', b'INTERNAL SERVER ERROR'))
    writer.write(status_line)
    headers = convert_headers_mapping_to_bytes({
        'Content-Encoding': 'utf-8',
        'Content-Type': "text/plain; charset=utf-8",
        'Date': dt.datetime.now().isoformat()
    })
    writer.write(headers)
    await writer.drain()
    writer.write(CRLF)
    writer.write(bytes(error_message, 'utf-8'))
    await writer.drain()
    return