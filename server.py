from chatroom import Chatroom
from client import Client, ChatroomClient
import threading
import socket

class Server:
    def __init__(self, ip_addr, port_num, student_id, socket):
        self.sock = socket
        self.server_alive_lock = threading.RLock()
        self.server_alive = True
        self.ip_addr = ip_addr
        self.port_num = port_num
        self.student_id = student_id
        self.chatrooms_lock = threading.RLock()
        self.chatrooms = {}
        self.clients_lock = threading.RLock()
        self.clients = []

    def kill_server(self):
        self.server_alive_lock.acquire()
        self.server_alive = False
        self.server_alive_lock.release()
        self.sock.close()

    def is_server_alive(self):
        return self.server_alive

    def _get_chatroom_by_name(self, name):
        for _, chatroom in self.chatrooms.iteritems():
            if chatroom.name == name:
                return chatroom

    def _create_chatroom(self, name):
        self.chatrooms_lock.acquire()
        chatroom = self._get_chatroom_by_name(name)
        
        if chatroom is None:
            room_ref = str(len(self.chatrooms) + 1)
            chatroom = Chatroom(name, room_ref)
            self.chatrooms[room_ref] = chatroom

        self.chatrooms_lock.release()

        return chatroom

    def add_client(self, connection):
        self.clients_lock.acquire()

        join_id = str(len(self.clients))
        client = Client(join_id, connection)
        self.clients.append(client)

        self.clients_lock.release()

        return client

    def join_chatroom(self, client, server, chatroom_name, client_ip_addr, client_port_num, client_name):
        chatroom = self._get_chatroom_by_name(chatroom_name)
        if chatroom is None:
            print 'Creating chatroom with name:', chatroom_name
            chatroom = self._create_chatroom(chatroom_name)

        chatroom.update_or_add_client(client, server, client_ip_addr, client_port_num, client_name)

        return client.connection.getsockname()[1], chatroom.ref, client.join_id

    def leave_chatroom(self, client, room_ref, join_id, client_name, disconnect=False):
        print 'looking for room:', room_ref
        print 'with chatrooms:', self.chatrooms
        chatroom = self.chatrooms.get(room_ref)
        if not chatroom:
            pass # return chatroom doesn't exist error
        else:
            if not disconnect:
                client.msg("LEFT_CHATROOM: {0}\nJOIN_ID: {1}\n".format(
                    room_ref, join_id))
            chatroom.msg("CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {2} has left this chatroom.\n\n".format(
                room_ref, client_name, client_name))
            chatroom.remove_client(join_id)
            return room_ref, join_id

    def disconnect(self, client, client_ip_addr, client_port_num, client_name):
        client.disconnect()

    def send_msg(self, client, room_ref, join_id, client_name, msg):
        chatroom = self.chatrooms.get(room_ref)
        if not chatroom:
            pass # return chatroom doesn't exist error
        else:
            chatroom.msg("CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {2}".format(
                room_ref, client_name, msg))
            return room_ref, client_name, msg
