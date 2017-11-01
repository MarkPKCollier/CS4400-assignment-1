from client import ChatroomClient
import threading

class Chatroom:
    def __init__(self, name, ref):
        self.name = name
        self.ref = ref
        self.clients_lock = threading.RLock()
        self.clients = []

    def add_client(self, chatroom_client):
        self.clients.append(chatroom_client)

    def update_or_add_client(self, client, client_ip_addr, client_port_num, client_name):
        self.clients_lock.acquire()

        matching_clients = filter(lambda client: client.name == client_name, self.clients)
        if matching_clients:
            client = matching_clients[0]
            client.ip_addr = client_ip_addr
            client.port_num = client_port_num
            client.name = client_name
        else:
            client = ChatroomClient(client, client_ip_addr, client_port_num, client_name)
            self.add_client(client)

        self.clients_lock.release()

    def remove_client(self, join_id):
        self.clients_lock.acquire()

        matching_clients = filter(lambda client: client.client.join_id == join_id, self.clients)
        for client in matching_clients:
            self.clients.remove(client)

        self.clients_lock.release()

    def msg(self, s):
        for client in self.clients:
            client.msg(s)