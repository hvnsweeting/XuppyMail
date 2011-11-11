#!/usr/bin/python

import simple_smtp

sender = 'hvn@familug.com'
receivers = ['hvnsweeting@hvn.vn']

message = """From: From Person <hvn@familug.com>
To: To Person <hvnsweeting@hvnbox>
Subject: First test my simple SMTP
"""

try:
   smtpObj = simple_smtp.SMTP('localhost', 25)
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"

#Output
#From hvn@familug.com  Sun Oct 16 13:35:16 2011
#Return-Path: <hvn@familug.com>
#X-Original-To: famihug@hvn.vn
#Delivered-To: famihug@hvn.vn
#Received: from hvn.vn (unknown [IPv6:::1])
#	by FamiHugK42F (Postfix) with ESMTP id E0DB041A87
#		for <famihug@hvn.vn>; Sun, 16 Oct 2011 13:35:15 +0700 (ICT)
#		From: From Person <hvn@familug.com>
#		To: To Person <famihug@hvn.vn>
#		Subject: Lai bao la khong gui duoc di
#		Message-Id: <20111016063515.E0DB041A87@FamiHugK42F>
#		Date: Sun, 16 Oct 2011 13:35:15 +0700 (ICT)
#
#		Cai nay chay ngon :))
