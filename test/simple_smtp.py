import socket

SMTP_PORT = 25

class SMTP:
	helo_resp = None
	def __init__(self, host='', port=0, local_hostname=None):
		#empty

	#moi ham tuong ung voi 1 SMTP command
	def sendmail(self, from_addr, to_addrs, msg):
		#empty
	def helo(self, name=''):
		#empty
	def mail(self, sender):
		#empty
	def rcpt(self, recip):
		#empty
	def data(self,msg):
		#empty
	def quit(self):
		#empty
