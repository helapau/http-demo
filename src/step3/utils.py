def is_empty(p):
    is_none = p is None
    is_empty = False
    if hasattr(p, "__len__"):
        is_empty = len(p) == 0
    return is_none or is_empty

CRLF = b"\r\n"

def print_headers(headers: dict) -> None:
    for k in headers:
        print(k.decode(), ": ", ", ".join([v.decode() for v in headers[k]]))
    print("\n")