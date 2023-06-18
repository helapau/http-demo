import asyncio
import datetime as dt
from pathlib import Path
import traceback

from step3.utils import CRLF, print_headers
import common
from step3.response_parser import parse_request_line, parse_headers, StatusLine, convert_first_line_to_bytes, \
    convert_headers_mapping_to_bytes


async def handle_login(reader, writer):
    status_line = convert_first_line_to_bytes(StatusLine(b'HTTP/1.0', b'200', b'OK'))
    headers = convert_headers_mapping_to_bytes({
        'Content-Encoding': 'utf-8',
        'Content-Type': "text/html; charset=utf-8",
        'Date': dt.datetime.now().isoformat(),
        'Set-Cookie': "sessionId=1234"
    })
    login_page_path = Path(__file__).parent / "vulnerable_login_page.html"
    with open(login_page_path, mode='rb') as fh:
        body = fh.read()
    writer.write(status_line)
    await writer.drain()
    writer.write(headers)
    await writer.drain()
    writer.write(CRLF)
    writer.write(body)
    await writer.drain()
    return

async def handle_pay(reader, writer):
    request_headers = await parse_headers(reader)
    body = bytes(''.join(
        [
            f"POST request to endpoint /pay came with the following headers:\n",
            "\n".join([f"{key.decode()}: {'; '.join([v.decode() for v in request_headers[key]])}" for key in request_headers])
        ]), 'utf-8')

    status_line = convert_first_line_to_bytes(StatusLine(b'HTTP/1.0', b'200', b'OK'))
    writer.write(status_line + CRLF)
    await writer.drain()
    response_headers = convert_headers_mapping_to_bytes({
        'Content-Encoding': 'utf-8',
        'Content-Type': "text/plain; charset=utf-8",
        'Date': dt.datetime.now().isoformat()
    })
    writer.write(response_headers + CRLF)
    await writer.drain()
    writer.write(body)
    await writer.drain()
    return

async def handler(reader, writer):
    try:
        raw_request_line = await reader.readuntil(CRLF)
        request_line = parse_request_line(raw_request_line)

        if request_line.method == b'GET' and request_line.request_target == b"/login":
            await handle_login(reader, writer)
        elif request_line.method == b'POST' and request_line.request_target == b'/pay':
            await handle_pay(reader, writer)
        else:
            await common.handle_not_found(writer)
    except Exception:
        await common.handle_internal_server_error(writer, traceback.format_exc(5))
    finally:
        writer.close()
        await writer.wait_closed()
        return



async def main():
    server = await asyncio.start_server(handler, '127.0.0.1', 9999)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving vulnerable site on {addrs}")
    async with server:
        await server.serve_forever()