#!/usr/bin/env python

"""Unpack a MIME message into a directory of files."""

import os
import sys
import email
import errno
import mimetypes

from optparse import OptionParser



def download(msg, desDir, fileNr):
    fileNr = int(fileNr)
    counter = 1
    for part in msg.walk():
        # multipart/* are just containers
        if part.get_content_maintype() == 'multipart':
            continue

		#down 1 file if fileNr is the number of file, down all if fileNr == 1000
        if fileNr != 1000:
            if counter != (fileNr + 2): #TODO clarify this line. just because it work, not really understand
                counter += 1
                continue
        # Applications should really sanitize the given filename so that an
        # email message can't be used to overwrite important files
        filename = part.get_filename()
        #print "Download file ", filename
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                # Use a generic bag-of-bits extension
                ext = '.bin'
            filename = 'part-%03d%s' % (counter, ext)
        counter += 1
		#TODO multiprocessing
        fp = open(os.path.join(desDir, filename), 'wb')
        fp.write(part.get_payload(decode=True))
        fp.close()


if __name__ == '__main__':
	msgfile = '/var/mail/famihug'
	fp = open(msgfile)
	msg = email.message_from_file(fp)
	fp.close()
	desDir = '/home/famihug/out/'
	download(msg, desDir, 2)
	print "Done!"

