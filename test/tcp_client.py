#example

import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5000))
while True:
	data = client_socket.recv(512)
	if data == 'q' or data == 'Q':
		client_socket.close()
		break;
	else:
		print "Received: ", data
		data = raw_input ("SEND(Type q or Q to quit):")
		if data <> 'Q' and data <> 'q':
			client_socket.send(data)
		else:
			client_socket.send(data)
			client_socket.close()
			break;
