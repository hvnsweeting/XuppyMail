#!/usr/bin/env python

import socket
import sys import stderr

POP3_PORT = 110
CRLF = "\r\n"

class POP3Exception(Exception):
	"""Base class"""

class POP3:
	"""Implement POP3"""
	def __init__(self):
		#TODO

	def user(self, username):
		sock.send('USER ' + username +"" + CRLF)
		(code, msg) = sock.recv(1000)#TODO separate code and msg

	def pass(self, password):
		sock.send('PASS ' + password + "" + CRLF)

	def list(self):
		sock.send('LIST')

	def retr(self, id):
		sock.send('RETR ' + id + "" + CRLF)

	def quit(self):
		sock.send('QUIT' + CRLF)

