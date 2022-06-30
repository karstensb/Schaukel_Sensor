import socket
import random
import time

HOST = "localhost"
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		s.send(b'%4.2f;'%random.random())
		time.sleep(random.random())