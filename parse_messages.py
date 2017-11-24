from abc import ABCMeta, abstractmethod
import re

# abstract class for message types
class Msg:
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse_msg(self, s):
        pass

    @abstractmethod
    def process(self, client, server):
        pass

class KillServiceMsg(Msg):
    def parse_msg(self, s):
        pattern = r"KILL_SERVICE\n"
        match = re.match(pattern, s)
        if match:
            return True, re.split(pattern, s)[-1]
        else:
            return False, s

    def process(self, client, server):
        pass

class HelloMsg(Msg):
    def parse_msg(self, s):
        pattern = r"HELO (.+)\n"
        match = re.match(pattern, s)
        if match:
            self.text = match.groups()[0]
            return self, re.split(pattern, s)[-1]
        else:
            return None, s

    def process(self, client, server):
        client.msg("HELO {0}\nIP:{1}\nPort:{2}\nStudentID:{3}\n".format(
            self.text, server.ip_addr, server.port_num, server.student_id))

class JoinChatroomMsg(Msg):
    def parse_msg(self, s):
        pattern = r"JOIN_CHATROOM: (.+)\nCLIENT_IP: (.+)\nPORT: (\d)+\nCLIENT_NAME: (.+)\n$"
        match = re.match(pattern, s)
        if match:
            self.chatroom_name, self.client_ip_addr, self.client_port_num, self.client_name = match.groups()
            return self, re.split(pattern, s)[-1]
        else:
            return None, s

    def process(self, client, server):
        self.chatroom_port_num, self.room_ref, self.join_id = server.join_chatroom(client,
            server, self.chatroom_name, self.client_ip_addr, self.client_port_num,
            self.client_name)

class LeaveChatroomMsg(Msg):
    def parse_msg(self, s):
        pattern = r"LEAVE_CHATROOM: (\d+)\nJOIN_ID: (\d+)\nCLIENT_NAME: (.+)\n$"
        match = re.match(pattern, s)
        if match:
            self.room_ref, self.join_id, self.client_name = match.groups()
            return self, re.split(pattern, s)[-1]
        else:
            return None, s

    def process(self, client, server):
        self.room_ref, self.join_id = server.leave_chatroom(client, self.room_ref, self.join_id, self.client_name)

class DisconnectMsg(Msg):
    def parse_msg(self, s):
        pattern = r"DISCONNECT: (.+)\nPORT: (\d+)\nCLIENT_NAME: (.+)\n$"
        match = re.match(pattern, s)
        if match:
            self.client_ip_addr, self.client_port_num, self.client_name = match.groups()
            return self, re.split(pattern, s)[-1]
        else:
            return None, s

    def process(self, client, server):
        for chatroom in filter(lambda chatroom: any(map(lambda client_: client.join_id == client_.client.join_id, chatroom.clients)), server.chatrooms.values()):
            server.leave_chatroom(client, chatroom.ref, client.join_id, self.client_name, disconnect=True)
        server.disconnect(client, self.client_ip_addr, self.client_port_num, self.client_name)

class ChatMsg(Msg):
    def parse_msg(self, s):
        pattern = r"CHAT: (\d+)\nJOIN_ID: (\d+)\nCLIENT_NAME: (.+)\nMESSAGE: (.+\n\n)$"
        match = re.match(pattern, s)
        if match:
            self.room_ref, self.join_id, self.client_name, self.msg = match.groups()
            return self, re.split(pattern, s)[-1]
        else:
            return None, s

    def process(self, client, server):
        self.room_ref, self.client_name, self.msg = server.send_msg(client, self.room_ref, self.join_id, self.client_name, self.msg)

class ErrorMsg(Msg):
    def parse_msg(self, s):
        pattern = r"(.+)\n"
        match = re.match(pattern, s)
        if match:
            return self, re.split(pattern, s)[-1]
        else:
            return None, s

    def process(self, client, server):
        client.msg("ERROR_CODE: 200\nERROR_DESCRIPTION: illegal message\n")

