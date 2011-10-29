import socket
"""Implement SMTP - reinvent the wheel"""

SMTP_PORT = 25

class SMTP:
	helo_resp = None
	def __init__(self, host='', port=0, local_hostname=None):
		#empty

	
	def getreply:
		#TODO
	
	def putcmd(self, cmd, args = ""):
		if args == "":
			str = '%s%s' % (cmd, CRLF)
		else:
			str = '%s %s %s' % (cmd, args, CRLF)
		self.send(str)
		#end putcmd

	def docmd(self, cmd, args = ""):
		"""Send a command and return its response code"""
		self.putcmd(cmd, args)
		return self.getreply()
	
	#moi ham tuong ung voi 1 SMTP command
	def sendmail(self, from_addr, to_addrs, msg):
		#empty

	def helo(self, name=''):
		"""SMTP 'helo' command.
		default hostname to send defaults to the FQDN of the localhost.		"""
		self.putcmd("HELO", name or self.local_hostname)
		(code, msg) = self.getreply()
		self.helo_resp = msg
		return (code, msg)

	def mail(self, sender):
		""" SMTP 'MAIL' command"""
		self.putcmd("MAIL", "FROM:%s" % (quoteaddr(sender)))
		return self.getreply()

	def rcpt(self, recip):
		""" SMTP 'RCPT' command """
		self.putcmd("RCPT", "TO:%s" % (quoteaddr(recip)))
		return self.getreply()

	def data(self,msg):
		self.putcmd("DATA")
		(code, repl) = self.getreply()
		#TODO
		#empty

	def quit(self):
		"""Terminate the SMTP session."""
		res = self.docmd("quit")
		self.close() #TODO implement later
		return res
