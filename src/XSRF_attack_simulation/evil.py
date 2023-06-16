import asyncio
from pathlib import Path
import datetime as dt

import common
from step3.utils import CRLF, print_headers
from step3.response_parser import convert_first_line_to_bytes, StatusLine, convert_headers_mapping_to_bytes, \
    parse_request_line, parse_headers


async def handle_get(writer):
    status_line = convert_first_line_to_bytes(StatusLine(b'HTTP/1.0', b'200', b'OK'))
    headers = convert_headers_mapping_to_bytes({
        'Content-Encoding': 'utf-8',
        'Content-Type': "text/html; charset=utf-8",
        'Date': dt.datetime.now().isoformat()
    })
    evil_page_path = Path(__file__).parent / "evil_page.html"
    with open(evil_page_path, mode='rb') as fh:
        body = fh.read()
    writer.write(status_line)
    await writer.drain()
    writer.write(headers)
    await writer.drain()
    writer.write(CRLF)
    writer.write(body)
    await writer.drain()
    return

async def handle_post(reader, writer):
    request_headers = await parse_headers(reader)
    print(f"Request headers to evil site POST handler:\n")
    print_headers(request_headers)
    await handle_get(writer)
    return

async def handler(reader, writer):
    raw_request_line = await reader.readuntil(CRLF)
    request_line = parse_request_line(raw_request_line)
    if request_line.method == b'GET':
        await handle_get(writer)
    elif request_line.method == b'POST':
        await handle_post(reader, writer)
    else:
        await common.handle_not_found(writer)

    writer.close()
    await writer.wait_closed()
    return

async def main():
    server = await asyncio.start_server(handler, 'localhost', 9998)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving evil site on {addrs}")
    async with server:
        await server.serve_forever()