import parse_messages as pm
from server import Server
import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port_num', type=int)
args = parser.parse_args()

student_id = 13319741

def handle_client(client, server):
    try:
        def parse_string(obj, s):
            obj, rem_msg = obj.parse_msg(msg)
            if obj:
                obj.process(client, server)
            return rem_msg

        msg = ''
        while True:
            msg += client.connection.recv(1024)
            t, msg = pm.KillServiceMsg().parse_msg(msg)
            if t:
                return -1
            msg_types = [pm.HelloMsg(), pm.JoinChatroomMsg(), pm.LeaveChatroomMsg(), pm.DisconnectMsg(), pm.ChatMsg()]
            for obj in msg_types:
                msg = parse_string(obj, msg)
    finally:
        client.connection.close()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', args.port_num))
    sock.listen(1)

    server = Server('localhost', args.port_num, student_id)

    while True:
        connection, addr = sock.accept()
        
        client = server.add_client(connection)
        res = handle_client(client, server)

        if res == -1:
            break
finally:
    sock.close()

