class Client:
    def __init__(self, join_id):
        self.join_id = join_id

class ChatroomClient:
    def __init__(self, client, ip_addr, port_num, name):
        self.client = client
        self.ip_addr = ip_addr
        self.port_num = port_num
        self.name = name

    def msg(self, s):
        pass