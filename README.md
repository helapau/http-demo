### Learn HTTP

To use TCP - send/receive bytes to/from a network socket.
A socket is an abstraction provided by your operating system that allows you to send and receive bytes through a network.
TCP socket = IP address + port

****
Questions:
* server = await asyncio.start_server(client_callback, 'localhost', 9000)
server.sockets = ('127.0.0.1', 9000), ('::1', 9000, 0, 0)
? what is the other socket?

* why is there a need to await StreamWriter.drain() after writing to it?
concpet of a IO buffer...?

* example code on https://docs.python.org/3/library/asyncio-stream.html#examples
in the handle_client_callback function the writer is closed also..why does the server need to do that?

* HTTP is text - what is the role of \r ? 





