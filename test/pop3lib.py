#!/usr/bin/env python

import socket
import re #regexp

#Standard port
POP3_PORT = 110

#Line terminator
CR = '\r'
LF = '\n'
CRLF = CR+LF

class error_proto(Exception):
	"""Base class"""
	pass

class POP3:
	"""Implement POP3"""
	def __init__(self, host='localhost', port=POP3_PORT, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
		self.host = host
		self.port = port
		self.sock = socket.create_connection((host, port), timeout)
		self.file = self.sock.makefile('rb')
		self._debugging = 0
		self.welcome = self._getresp()

	def _putline(self, line):
		if self._debugging > 1: print '*put', repr(line)
		self.sock.sendall('%s%s' % (line, CRLF))

	def _putcmd(self, line):
		if self._debugging > 1: print '*cmd', repr(line)
		self._putline(line)

	def _getline(self):
		line = self.file.readline()
		if self._debugging > 1: print '*get*', repr(line)
		if not line: raise error_proto('-ERR EOF')
		octets = len(line)
		#server send combination of CR & LF
		#'readline()' returns lines ending in LF
		# Return line with strip of line terminator
		if line[-2:] == CRLF: #because python treat \n = 1 char \r = 1 char
			return line[:-2], octets
		if line[0] == CR:
			return line[1:-1], octets

	def _getresp(self):
		""" Get a response from the server.
	 Raise 'error_proto' if response doesn't start with '+'"""
		resp, o = self._getline()
		if self._debugging > 1: print '*resp*', repr(resp)
		c = resp[:1]#get first return char
		if c != '+':
			raise error_proto(resp)
		return resp

#	def _getresp(self):
#		resp, o = self._getline()
#		if self._debugging > 1: print '*resp*', repr(resp)
#		c = resp[:1]
#		if c != '+':
#			print resp
#		    #raise error_proto(resp)
#		return resp

	def _getlongresp(self):
		resp = self._getresp()
		li = []
		octets = 0
		line, o = self._getline()
		while line != '.':
			if line[:2] == '..':
				o = o - 1
				line = line[1:]
			octets = octets + o
			li.append(line)
			line, o = self._getline()
		return resp, li, octets

	def _shortcmd(self, line):
		"""Send a command and get the response"""
		self._putcmd(line)
		return self._getresp()

	def _longcmd(self, line):
		self._putcmd(line)
		return self._getlongresp()

	def getwelcome(self):
		"""Get name of service MTA"""
		return self.welcome

	def set_debuglevel(sefl, level):
		self._debugging = level

	#POP3 Command
	def user(self, username):
		"""Send user name, return response"""
		return self._shortcmd('USER %s' % username)

	def pass_(self, password):
		"""pass_ because pass is Python reserved word"""
		return self._shortcmd('PASS %s' % password)

#	def stat(self):
#		"""Get mailbox status.
#	
#		Result is tuple of 2 ints (message count, mailbox size)
#		"""
#		retval = self._shortcmd('STAT')
#		rets = retval.split()
#		if self._debugging: print '*stat*', repr(rets)
#		numMessages = int(rets[1])
#		sizeMessages = int(rets[2])
#		return (numMessages, sizeMessages)
	def stat(self):
		"""Get mailbox status
		return is tuple of 2 ints (message count, mailbox size)
		"""
		retval = self._shortcmd('STAT')
		rets = retval.split()
		if self._debugging: print '*stat*', repr(rets)
		#rets[0] is '+OK'
		numMsgs = int(rets[1])
		sizeMsgs = int(rets[2])
		return (numMsgs, sizeMsgs)

	def list(self, which=None):
		"""Request listing, return result
		if a msg number is given, return the "scan listing" for that msg
		"""
		if which is not None:
			return self._shortcmd('LIST %s', which)
		return self._longcmd('LIST')

	def retr(self, which):
		"""Retrieve whole msg number 'which'
		Result is in form ['response', ['line',...], octets]
		"""
		return self._longcmd('RETR %s' % which)

	def dele(self, which):
		"""Delete msg number 'which'
		Result is response
		"""
		return self._shortcmd('DELE %s' % which)

	def noop(self):
		"""Does nothing.

	`	One supposes the response indicates the server is alive.
		"""
		return self._shortcmd('NOOP')


	def rset(self):
		"""Unmark all messages marked for deletion."""
		return self._shortcmd('RSET')


	def quit(self):
		"""Signoff: commit changes on server, unlock mailbox, close connection."""
		try:
			resp = self._shortcmd('QUIT')
		except error_proto, val:
			resp = val
		self.file.close()
		self.sock.close()
		del self.file, self.sock
		return resp
