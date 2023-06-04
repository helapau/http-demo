def is_empty(p):
    is_none = p is None
    is_empty = False
    if hasattr(p, "__len__"):
        is_empty = len(p) == 0
    return is_none or is_empty

CRLF = b"\r\n"