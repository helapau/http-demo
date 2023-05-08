import asyncio

# headers+body..

def handle_get(reader, writer):
    # assume the request is correct lol
    html_text = []
    with open("home.html", 'r') as fh:
        html_text = fh.readlines()
    print("".join(html_text))


handle_get(None, None)