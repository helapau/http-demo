from dataclasses import dataclass, field
import re

from utils import is_empty

class ParseError(Exception):
    def __init__(self, message):
        self.message = message

@dataclass
class Response:
    http_version: field(default_factory=str)
    status_code: field(default=None)
    status_message: field(default_factory=str)
    headers: field(default_factory=dict)

    raw_body: field(default_factory=str)

    def __str__(self):
        def display_headers():
            lines = []
            for key in self.headers:
                lines.append(f"\t{key}: {self.headers[key]}")
            return "\n".join(lines)
        return "\n".join((f"HTTP version: {self.http_version}",
                          f"status code: {self.status_code}",
                          f"reason: {self.status_message}",
                          f"headers:\n {display_headers()}",
                          f"raw body: {self.raw_body}"))


def parse_status_line(first_line: str) -> tuple:
    # specification defines syntax: (*optional)
    # HTTP-version[SP]status-code[SP]reason*
    first_line = first_line.strip("[\r\n]")
    groups = first_line.split(" ", 1)
    if len(groups) < 2:
        raise ParseError("Error parsing status line - expected 2 or 3 strings separated by a single SP character.")
    try:
        protocol, http_version = groups[0].split("/")
    except ValueError:
        raise ParseError("Error parsing status line - expected format {protocol}/{version}")
    code_match = re.search(r'(\d{3})', groups[1])
    if code_match is None:
        raise ParseError("Invalid characters in HTTP status code")
    status_code = code_match.group()
    status_message = groups[1][code_match.end():].strip()
    if is_empty(status_message):
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
    if is_empty(body):
        body = None

    return Response(http_version, status_code, status_message, headers_map, body)