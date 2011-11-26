#!/usr/bin/env python
# vim:fileencoding=utf8

from email.Header import decode_header
import email
from base64 import b64decode
import sys
from email.Parser import Parser as EmailParser
from email.utils import parseaddr
from StringIO import StringIO
from time import strptime, strftime

class NotSupportedMailFormat(Exception):
    pass

def parse_attachment(message_part):
    content_disposition = message_part.get("Content-Disposition", None)
    if content_disposition:
        dispositions = content_disposition.strip().split(";")
        if bool(content_disposition and dispositions[0].lower() == "attachment"):

            file_data = message_part.get_payload(decode=True)
            attachment = StringIO(file_data)
            attachment.content_type = message_part.get_content_type()
            attachment.size = len(file_data)
            attachment.name = None
            attachment.create_date = None
            attachment.mod_date = None
            attachment.read_date = None

            for param in dispositions[1:]:
                name,value = param.split("=")
                name = name.lower()

                if name == " filename": #must have the space before filename
                    #attachment.name = value
                    attachment.name = message_part.get_filename()
                elif name == "create-date":
                    attachment.create_date = value  #TODO: datetime
                elif name == "modification-date":
                    attachment.mod_date = value #TODO: datetime
                elif name == "read-date":
                    attachment.read_date = value #TODO: datetime
            return attachment

    return None

def parse_date(time):
	"""Parse RFC2822 time format to %Y/%m/%d %H:%M:%S"""
	if time is None:
		return None
	else:
		stripoff = time.split('+')
		t = strptime(stripoff[0], "%a, %d %b %Y %H:%M:%S ")
		return strftime("%Y/%m/%d %H:%M:%S", t)

def parse(content):
    """
	parse email
    """
    p = EmailParser()
	#check content is a file or text
	#if content is path...

    #msgobj = p.parse(content)
	
    msgobj = p.parsestr(content)
    if msgobj['Subject'] is not None:
        decodefrag = decode_header(msgobj['Subject'])
        subj_fragments = []
        for s , enc in decodefrag:
            if enc:
                s = unicode(s , enc).encode('utf8','replace')
            subj_fragments.append(s)
        subject = ''.join(subj_fragments)
    else:
        subject = None

    attachments = []
    body = None
    html = None
    for part in msgobj.walk():
        attachment = parse_attachment(part)
        if attachment:
            attachments.append(attachment)
        elif part.get_content_type() == "text/plain":
            if body is None:
                body = ""
                if part.get_content_charset:
                    body += part.get_payload(decode=True)
                else:
                    body += unicode(
                    part.get_payload(decode=True),
                    part.get_content_charset(),
                'replace'
            ).encode('utf8','replace')
        elif part.get_content_type() == "text/html":
            if html is None:
                html = ""
            html += unicode(
                part.get_payload(decode=True),
                part.get_content_charset(),
                'replace'
            ).encode('utf8','replace')
    return {
        'subject' : subject,
        'body' : body,
        'html' : html,
        'from' : parseaddr(msgobj.get('From'))[1], 
        'to' : parseaddr(msgobj.get('To'))[1], 
		'date' : parse_date(msgobj.get('Date')),
        'attachments': attachments,
    }

if __name__ == '__main__':
	fp = open('/var/mail/famihug', 'r')
	info = parse(fp)
	print info['date'] 
	print info['subject']
	print info['from']
	print info['to']
	print info['body']
	print 'Number of attachments: ', len(info['attachments'])
