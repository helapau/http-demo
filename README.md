### Learn HTTP

## step 1
TCP client and server 

## step2
Send HTTP GET request over TCP

## step 3
Sending more requests and parsing the response.

## Simulate a cross site request forgery attack:
Open the browser and navigate to `127.0.0.1:9999/login` to receive a cookie sessionId=1234.
In another tab, navigate to `localhost:9998/` here are two buttons. 
The first one simulates the attack - it sends a POST request to `127.0.0.1:9999/pay` 
and browser sends the sessionId cookie because request was made to the domain `127.0.0.1` 
where the cookie belongs. 
The other button only sends POST to the current domain `localhost` - check that the sessionId cookie 
from `127.0.0.1` is *not* sent with the request.

Notes:
- Cookies do not provide isolation by port. 
- instead of `localhost` domain name for the evil site, we could have used alo `127.0.0.2`, `127.0.0.3`, 
   it would also be a different address

Todos/fixmes:
- Exceptions?? 
- after the "attack" button is clicked/form is submitted, how to prevent the page from redirecting?

