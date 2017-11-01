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

    def update_or_add_client(self, client, server, client_ip_addr, client_port_num, client_name):
        self.clients_lock.acquire()

        matching_clients = filter(lambda client: client.name == client_name, self.clients)
        if matching_clients:
            client_ = matching_clients[0]
            client_.ip_addr = client_ip_addr
            client_.port_num = client_port_num
            client_.name = client_name
        else:
            client_ = ChatroomClient(client, client_ip_addr, client_port_num, client_name)
            self.add_client(client_)

        client.msg("JOINED_CHATROOM: {0}\nSERVER_IP: {1}\nPORT: {2}\nROOM_REF: {3}\nJOIN_ID: {4}\n".format(
            self.name, server.ip_addr, client.connection.getsockname()[1],
            self.ref, client.join_id))
        self.msg("CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {2} has joined this chatroom.\n\n".format(
            self.ref, client_name, client_name))

        self.clients_lock.release()

    def remove_client(self, join_id):
        self.clients_lock.acquire()

        print 'clients before removal', self.clients
        print 'join id', join_id, type(join_id)
        print map(lambda client: (client.client.join_id, type(client.client.join_id)), self.clients)
        self.clients = filter(lambda client: client.client.join_id != join_id, self.clients)
        # print 'clients before removal', self.clients
        # for client in matching_clients:
        #     print 'client to be removed', client
        #     self.clients.remove(client)
        print 'clients after removal', self.clients

        self.clients_lock.release()

    def msg(self, s):
        for client in self.clients:
            print 'sending msg:', s, 'to :', client.name
            client.msg(s)