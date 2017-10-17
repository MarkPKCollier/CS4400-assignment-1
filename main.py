import parse_messages as pm
from server import Server
import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port_num', type=int)
args = parser.parse_args()

student_id = 13319741

def handle_client(client):
    def parse_string(obj, s):
        obj, rem_msg = obj.parse_message(msg)
        if obj:
            obj.side_effect(client, msg).response(msg)
        return rem_msg

    msg = ''
    while True:
        msg += client.connection.recv(1024)
        msg_types = [pm.KillServiceMsg(), pm.HelloMsg(), pm.JoinChatroomMsg(), pm.LeaveChatroomMsg(), pm.DisconnectMsg(), pm.ChatMsg()]
        for obj in msg_types:
            msg = parse_string(obj, msg)

s = socket.socket()
ip_addr = socket.gethostname()
print 'ip_addr', ip_addr
s.bind((ip_addr, args.port_num))

server = Server(ip_addr, args.port_num, student_id)

while True:
    connection, addr = s.accept()
    
    client = server.add_client(connection)
    handle_client(client)

    connection.close()

