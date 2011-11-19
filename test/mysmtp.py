#!/usr/bin/env python

import socket
import email.utils
import re
from sys import stderr

"""Implement SMTP - reinvent the wheel"""

SMTP_PORT = 25
CRLF = "\r\n"

__all__ = ["SMTPException"]

class SMTPException(Exception):
	"""Base class"""

class SMTPServerDisconnected(SMTPException):
	"""Not connected to any SMTP server"""

class SMTPResponseException(SMTPException):
	def __init__(self, code, msg):
		self.smtp_code = code
		self.smtp_error = msg
		self.args = (code, msg)

class SMTPConnectError(SMTPResponseException):
	"""Error during connection establishment."""

def quoteaddr(addr):
	m = (None, None)
	try:
		m = email.util.parseaddr(addr)[1]
	except AttributeError:
		pass
	if m == (None, None):
		return "<%s>" % addr
	elif m is None:
		return "<>"
	else:
		return "<%s>" % m

def quotedata(data):
	return re.sub(r'(?m)^\.', '..', 
			re.sub(r'(?:\r\n|\n|\r(?!\n))', CRLF, data))

class SMTP:
	helo_resp = None
	file = None
	def __init__(self, host='', port=25, local_hostname=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
		self.timeout = timeout
		self.default_port = SMTP_PORT

		if host:
			(code, msg) = self.connect(host, port)
			if code != 220:
				raise SMTPConnectError(code, msg)

		if local_hostname is not None:
			self.local_hostname = local_hostname
		else:
			fqdn = socket.getfqdn()
			if '.' in fqdn:
				self.local_hostname = fqdn
			else:
				addr = '127.0.0.1'
				try:
					addr = socket.gethostbyname(socket.gethostbyname())
				except socket.gaierror:
					pass
				self.local_hostname = '[%s]' % addr

	def getreply(self):
		resp = []
		if self.file is None:
			self.file = self.sock.makefile('rb')
		while True:
			line = self.file.readline()
			if line == '':
				self.close()
				raise SMTPServerDisconnected("Connection unexpectedly closed")
			resp.append(line[4:].strip())
			code = line[:3]

			try:
				errcode = int(code)
			except ValueError:
				errcode = -1
				break

			if line[3:4] != "-":
				break

		errmsg = "\n".join(resp)
		return errcode, errmsg


	def _get_socket(self, port, host, timeout):
		return socket.create_connection((port, host), timeout)

	def connect(self, host = 'localhost', port = 0):
		"""Connect to a host on a given port"""
		self.sock = self._get_socket(host, port, self.timeout)
		(code, msg) = self.getreply()
		return (code, msg)

	
	def send(self, str):
		"""Send str to server"""
		if hasattr(self, 'sock') and self.sock:
			try:
				self.sock.sendall(str)
			except socket.error:
				self.close()
				raise SMTPServerDisconnected('Server not connected')
		else:
			raise SMTPServerDisconnected('Please run connect() first')
	
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

	def connect(self, host='localhost', port = 0):
		#connect to a given host
		self.sock = self._get_socket(host, port, self.timeout)
		(code, msg) = self.getreply()
		return (code, msg)
	
	#moi ham tuong ung voi 1 SMTP command
	def helo(self, name=''):
		"""SMTP 'helo' command.
		default hostname to send defaults to the FQDN of the localhost.		"""
		self.putcmd("helo", name or self.local_hostname)
		(code, msg) = self.getreply()
		self.helo_resp = msg
		return (code, msg)

	def mail(self, sender):
		""" SMTP 'MAIL' command"""
		self.putcmd("mail", "FROM:%s" % (quoteaddr(sender)))
		return self.getreply()

	def rcpt(self, recip):
		""" SMTP 'RCPT' command """
		self.putcmd("rcpt", "TO:%s" % (quoteaddr(recip)))
		return self.getreply()

	def data(self,msg):
		self.putcmd("data")
		(code, repl) = self.getreply()
		#TODO below code is bug
		#if code != 354:
		#	raise SMTPException#TODO change later
		q = quotedata(msg) 
		if q[-2:] != CRLF:
			q = q + CRLF
		q = q + "." + CRLF
		self.send(q)
		(code ,msg) = self.getreply()
		return (code, msg)

	def sendmail(self, from_addr, to_addrs, msg):
		self.helo()#TODO if needed
#		(code, resp) = self.mail(from_addr)
#		if code != 250:
#			raise SMTPSenderRefused(code, resp, from_addr)
#
#
#		to_addrs = to_addrs[0] #TODO sent to many recp
#		(code, resp) = self.rcpt(to_addrs)
#		if code != 250:
#		   raise SMTPServerDisconnected
#		
#		(code, resp) = self.data(msg)
#		if code != 250:
#			raise SMTPConnectError
#
#        self.ehlo_or_helo_if_needed()

		(code,resp) = self.mail(from_addr)
		if code != 250:
		    self.rset()
		    raise SMTPSenderRefused(code, resp, from_addr)
		senderrs={}
		if isinstance(to_addrs, basestring):
		    to_addrs = [to_addrs]
		for each in to_addrs:
			(code,resp)=self.rcpt(each)
			if (code != 250) and (code != 251):
				senderrs[each]=(code,resp)
		if len(senderrs)==len(to_addrs):
		    # the server refused all our recipients
		    self.rset()
		    raise SMTPRecipientsRefused(senderrs)
		(code,resp) = self.data(msg)
		if code != 250:
		    self.rset()
		    raise SMTPDataError(code, resp)
		#if we got here then somebody got our mail
		return senderrs

	def close(self):
		"""Close connection to the SMTP server"""
		if self.file:
			self.file.close()
		self.file = None
		if self.sock:
			self.sock.close()
		self.sock = None

	def quit(self):
		"""Terminate the SMTP session."""
		res = self.docmd("quit")
		self.close() #TODO implement later
		return res
