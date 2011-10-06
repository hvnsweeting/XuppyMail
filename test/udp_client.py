#Simple python datagram echo client
import socket

dsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

dsock.sendto("Hello\n", ('', 23456))
print "Received from server: " + dsock.recv(100)
dsock.close()
