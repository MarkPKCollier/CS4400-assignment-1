from abc import ABCMeta, abstractmethod
import re

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
            return KillServiceMsg(), re.split(pattern, s)[-1]
        else:
            return None, s

    def process(self, client, server):
        pass

class HelloMsg(Msg):
    def parse_msg(self, s):
        pattern = r"HELO text"
        match = re.match(pattern, s)
        if match:
            return self, re.split(pattern, s)[-1]
        else:
            return None, s

    def process(self, client, server):
        client.msg("HELO text\nIP:{0}\nPort:{1}\nStudentID:{2}\n".format(
            server.ip_addr, server.port_num, server.student_id))

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
            self.chatroom_name, self.client_ip_addr, self.client_port_num, self.client_name)
        client.msg("JOINED_CHATROOM: {0}\nSERVER_IP: {1}\nPORT: {2}\nROOM_REF: {3}\nJOIN_ID: {4}\n".format(
            self.chatroom_name, server.ip_addr, self.chatroom_port_num, self.room_ref, self.join_id))
        chatroom = server._get_chatroom_by_name(self.chatroom_name)
        chatroom.msg("{0} has joined this chatroom.\n\n".format(self.client_name))

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
        client.msg("LEFT_CHATROOM: {0}\nJOIN_ID: {1}\n".format(
            self.room_ref, self.join_id))

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
        server.disconnect(client, self.client_ip_addr, self.client_port_num, self.client_name)

class ChatMsg(Msg):
    def parse_msg(self, s):
        pattern = r"CHAT: (\d+)\nJOIN_ID: (\d+)\nCLIENT_NAME: (.+)\nMESSAGE: (.+\n\n)\n$"
        match = re.match(pattern, s)
        if match:
            self.room_ref, self.join_id, self.client_name, self.msg = match.groups()
            return self, re.split(pattern, s)[-1]
        else:
            return None, s

    def process(self, client, server):
        self.room_ref, self.client_name, self.msg = server.send_msg(client, self.room_ref, self.join_id, self.client_name, self.msg)
        client.msg("CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {2}\n".format(
            self.room_ref, self.client_name, self.msg))

# from server import Server
# from client import Client

# c = Client(1)
# s = Server('0.0.0.0', 8080, 13319741)

# tmp = ChatMsg()

# good_msg = "CHAT: 1\nJOIN_ID: 100\nCLIENT_NAME: mark collier\nMESSAGE: hello world\n\n\n"
# bad_msg = "I am very bad"

# print tmp.parse_msg(good_msg)
# print tmp.parse_msg(good_msg).side_effect(c, s).response(s)
# print tmp.parse_msg(bad_msg)

# data ErrorMsg = Error Int String
#             deriving (Show)

