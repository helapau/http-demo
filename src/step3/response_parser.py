from dataclasses import dataclass, field
import re

class ParseError(Exception):
    def __init__(self, message):
        self.message = message

@dataclass
class Response:
    http_version: field(default_factory=str)
    status_code: field(default=None)
    status_message: field(default_factory=str)
    headers: field(default_factory=dict)


def parse_status_line(first_line: str) -> tuple:
    # specification defines syntax: (*optional)
    # HTTP-version[SP]status-code[SP]reason*
    first_line = first_line.strip("[\r\n]")
    # fixme - splitting the line: as soon as you find a space - stop!
    groups = re.split(r" ", first_line)
    if len(groups) != 2 and len(groups) != 3:
        raise ParseError("Error parsing status line - expected 2 or 3 strings separated by a single SP character.")
    protocol_groups = groups[0].split("/")
    if len(protocol_groups) != 2:
        raise ParseError("Error parsing status line - expected format {protocol}/{version}")
    http_version = protocol_groups[1]
    try:
        status_code = int(groups[1])
    except ValueError:
        raise ParseError("Invalid characters in HTTP status code")
    if len(groups) == 3:
        status_message = groups[2]
    else:
        status_message = None

    return http_version, status_code, status_message

def parse_headers(headers: list):
    result = {}
    # syntax: field-name[space][:][space]value
    if len(headers) == 0:
        return result
    # might be any number of LWS around the `:` but a single space is preferred
    pattern = re.compile(r'(?:\s*:\s*)')
    for line in headers:
        groups = re.split(pattern, line)
        if len(groups) == 2:
            # found a key-value pair
            key = groups[0].strip().lower()
            value = groups[1].strip()
            if key not in result:
                result[key] = value
    return result

def parse_body(body: list):
    pass


def parse_response(response_lines: list):
    """
    :param response: full text of the response
    :return: instance of Response
    """
    start_line = response_lines.pop(0) if len(response_lines) > 0 else ""
    http_version, status_code, status_message = parse_status_line(start_line)

    # split response_lines into headers and body -> separated by an empty line containing only \r\n
    separator_index = -1
    separator_pattern = re.compile(r'\r\n')
    for i, l in enumerate(response_lines):
        if re.match(separator_pattern, l):
            separator_index = i
            break
    if separator_index == -1:
        raise ParseError("Could not split response into headers and body sections")
    headers = response_lines[0:separator_index]
    body = response_lines[separator_index + 1:]
    headers_map = parse_headers(headers)

    return Response(http_version, status_code, status_message, headers_map)