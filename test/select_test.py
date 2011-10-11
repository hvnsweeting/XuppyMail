import socket
import select

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock1.connect(('', 54321))
sock2.connect(('', 54321))

while True:
	rlist, wlist, elist = select.select( [sock1, sock2], [], [], 5)

	if [rlist, wlist, elist] == [[], [], []]:
		print "Five second elapsed"
	else:
		for sock in rlist:
			print sock.recv(100)

#hehehehe ta la Dung