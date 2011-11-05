#!/usr/bin/env python
import simple_smtp

sender = 'hvn@hehe.com'
receivers = ['famihug@hvn.vn']
message = 'Do re mi'
try:
	s = simple_smtp.SMTP('localhost', 25)
	s.sendmail(sender, receivers, message)
	print "done"
except SMTPException:
	print "err"
