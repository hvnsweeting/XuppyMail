
#Simple stream echo client
#This program quit after recieved message from server
import socket

#1: create a socket obj
#AF_INET indicates request an IP socket (IPv4). AF_INET6 for IPv6
#second arg: transport protocol type
ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP sockets

#2.Connect to an address+port
ssock.connect(('', 54321))

#3. Send message to server
ssock.send("Hello\n")

#4. Print the message recieved form server
print "Received from server: " + ssock.recv(100)

ssock.close()
