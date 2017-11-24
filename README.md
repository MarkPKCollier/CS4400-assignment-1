# CS4400-assignment-1

The structure of my solution is very simple.

I have a main program which listens for incoming connections on a specified port numbers.

It accepts new connections and hands them off to a separate thread (for each connection) which listens for incoming messages from that connection.

I use regular expressions to parse the incoming messages.

I take an object orientated approach to my design with classes for message types, the server, clients and the chatrooms.

This enables me to implement the monitor locking pattern, with each object maintaining locks internally and exposing methods which transparently maintain thread safe usage.

This solution always get's 100% on the provided test server.

## Errors

The error code 100 is used to signify that a specified chatroom does not exist.

The error code 200 is used to signify that a sent message was illegal.