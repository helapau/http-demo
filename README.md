### Learn HTTP

## talking over TCP
TCP client and server - just sending bytes.

## httpGET
Send HTTP GET request over TCP. HTTP is text!

## more HTTP
Sending more requests and parsing the response.

## cross-site
Explore cookies: if server includes header field `Set-Cookie` the client then includes the cookie in every subsequent request.
Navigating to `127.0.0.1:9999/login`, there are some scenarios for the CSRF attack.
Secure web browser implements the same-origin policy (same origin = schema, host & port) preventing the cookie to be shared
in the following examples:
- on load, a XMLHttpRequest is sent asynchronously (it *is* sent but without the cookie) - see console for message 
*Cross-Origin request blocked*
- `<form>` with `target` attribute set to a hidden iframe - cookie is not sent thanks to ???
Submitting form with action set to the vulnerable endpoint sends the cookie - but also opens the endpoint in a new tab.

Notes:
- Cookies do not provide isolation by port. 
- instead of `localhost` domain name for the evil site, we could have used also `127.0.0.2`, `127.0.0.3`, 
   it would also be a different address

