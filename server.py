class Server:
	def __init__(self, ip_addr, port_num, student_id):
		self.ip_addr = ip_addr
		self.port_num = port_num
		self.student_id = student_id

	def join_chatroom(self, chatroom_name, client_ip_addr, client_port_num, client_name):
		chatroom_port_num, room_ref, join_id = (1,2,3)

		return chatroom_port_num, room_ref, join_id

	def leave_chatroom(self, room_ref, join_id, client_name):
		return room_ref, join_id

	def disconnect(self, client_ip_addr, client_port_num, client_name):
		pass

	def send_msg(self, room_ref, join_id, client_name, msg):
		return room_ref, client_name, msg