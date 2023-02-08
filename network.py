import socket
import pickle

class Network:
	def __init__(self):
		self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host='152.89.237.254'
		self.port=48329
		self.addr = (self.host, self.port)
		self.p = self.connect()

	def getP(self):
		return self.p

	def connect(self):
		try:
			self.client.connect(self.addr)
			print("connected to", self.host)
			return pickle.loads(self.client.recv(2048))
		except:
			pass

	def send(self, data):
		try:
			self.client.send(pickle.dumps(data))
			return pickle.loads(self.client.recv(2048))
		except socket.error as e:
			print(e)

	def sendnoreturn(self, data):
		try:
			self.client.send(pickle.dumps(data))
		except socket.error as e:
			print(e)
