#Simple python datagram echo server
import socket

dsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dsock.bind(('',23456))

while True:
	msg, (addr, port) = dsock.recvfrom(100)
	print "Received msg: " + msg + "from " + addr + ":" + str(port)
	dsock.sendto(msg, (addr, port))
