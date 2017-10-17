from chatroom import Chatroom
from client import Client, ChatroomClient
import threading
import socket

class Server:
    def __init__(self, ip_addr, port_num, student_id):
        self.ip_addr = ip_addr
        self.port_num = port_num
        self.student_id = student_id
        self.chatrooms_lock = threading.RLock()
        self.chatrooms = {}
        self.clients_lock = threading.RLock()
        self.clients = []

    def _get_chatroom_by_name(self, name):
        for _, chatroom in self.chatrooms.iteritems():
            if chatroom.name == name:
                return chatroom

    def _create_chatroom(self, name):
        self.chatrooms_lock.acquire()
        chatroom = self._get_chatroom_by_name(name)
        
        if chatroom is None:
            room_ref = len(self.chatrooms) + 1
            chatroom = Chatroom(name, self.port_num, room_ref)

        self.chatrooms_lock.release()

        return chatroom

    def add_client(self, connection):
        self.clients_lock.acquire()

        join_id = len(self.clients)
        client = Client(join_id, connection)
        self.clients.append(client)

        self.clients_lock.release()

        return client

    def join_chatroom(self, client, chatroom_name, client_ip_addr, client_port_num, client_name):
        chatroom = self._get_chatroom_by_name(chatroom_name)
        if chatroom is None:
            chatroom = self._create_chatroom(chatroom_name)

        chatroom.update_or_add_client(client, client_ip_addr, client_port_num, client_name)

        return client.connection.getsockname()[1], chatroom.room_ref, client.join_id

    def leave_chatroom(self, client, room_ref, join_id, client_name):
        chatroom = self.chatrooms.get(room_ref)
        if not chatroom:
            pass # return chatroom doesn't exist error
        else:
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
