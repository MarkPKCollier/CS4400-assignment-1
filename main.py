import parse_messages as pm
from server import Server
import socket
import argparse
import thread
import logging

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('--port_num', type=int)
args = parser.parse_args()

student_id = 13319741

# instead of hard coding my public ip I discover it by making an external connection
# if you wish to hard code an ip address please replace this code
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
my_ip = s.getsockname()[0]
s.close()

logging.info('Starting server on: {0}'.format(my_ip))

def handle_client(client, server):
    '''A function which handles all messages from a single client.'''
    try:
        def parse_string(obj, s):
            '''Parse a string for a potential message and return the remaining string.'''
            obj, rem_msg = obj.parse_msg(msg)
            if obj:
                obj.process(client, server)
            return rem_msg

        msg = ''
        while server.is_server_alive():
            msg += client.connection.recv(1024)
            logging.info('msg: {0}'.format(msg))
            t, msg = pm.KillServiceMsg().parse_msg(msg)
            if t:
                server.kill_server()
            msg_types = [pm.HelloMsg(), pm.JoinChatroomMsg(), pm.LeaveChatroomMsg(), pm.DisconnectMsg(), pm.ChatMsg(), pm.ErrorMsg()]
            for obj in msg_types:
                msg = parse_string(obj, msg)
    finally:
        client.connection.close()

try:
    # socket setup
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.bind((my_ip, args.port_num))
    sock.listen(1)

    server = Server(my_ip, args.port_num, student_id, sock)

    while server.is_server_alive():
        try:
            # accept new connections and hand them off to a new thread
            connection, addr = sock.accept()
            client = server.add_client(connection)
            thread.start_new_thread(handle_client, (client, server))
        except socket.error:
            pass
finally:
    sock.close()

