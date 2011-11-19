
#Simple stream echo server
import socket

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
sock.bind( ('', 54321) )
sock.listen(5)

while True:
	newsock, (remhost, remport) = sock.accept()
	print "Connected to " + remhost + ":" + str(remport),
	message = newsock.recv(100)
	print " recieved from client: " + message
	newsock.send(message)
	newsock.close()
# tAO LA hUNG