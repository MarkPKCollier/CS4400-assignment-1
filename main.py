import parse_messages as pm
from server import Server
import socket
import argparse
import thread

parser = argparse.ArgumentParser()
parser.add_argument('--port_num', type=int)
args = parser.parse_args()

student_id = 13319741

class KillServer(Exception):
    def __init__(self):
        Exception.__init__(self)

def handle_client(client, server):
    print 'Handling new client'
    try:
        def parse_string(obj, s):
            obj, rem_msg = obj.parse_msg(msg)
            if obj:
                obj.process(client, server)
            return rem_msg

        msg = ''
        while server.is_server_alive():
            msg += client.connection.recv(1024)
            print 'msg:', msg
            t, msg = pm.KillServiceMsg().parse_msg(msg)
            if t:
                server.kill_server()
                raise KillServer()
            msg_types = [pm.HelloMsg(), pm.JoinChatroomMsg(), pm.LeaveChatroomMsg(), pm.DisconnectMsg(), pm.ChatMsg()]
            for obj in msg_types:
                msg = parse_string(obj, msg)
    finally:
        client.connection.close()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.bind(('134.226.44.50', args.port_num))
    sock.listen(1)

    server = Server('134.226.44.50', args.port_num, student_id, sock)

    while server.is_server_alive():
        try:
            connection, addr = sock.accept()
            client = server.add_client(connection)
            thread.start_new_thread(handle_client, (client, server))
        except KillServer:
            break
        except socket.error:
            pass
finally:
    sock.close()

