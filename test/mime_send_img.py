import smtplib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

msg = MIMEMultipart()
msg['Subject'] = 'Some pictures'
msg['From'] = 'anon@gmail.com'
msg['To'] = 'famihug@hvn.vn'
msg.preamble = 'test for fun'
pngfiles = ['IMG9040.JPG', 'IMG_9404.JPG']

for f in pngfiles:
	fp = open(f, 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)
	
s = smtplib.SMTP('localhost')
s.sendmail(msg['From'], msg['To'], msg.as_string())
print 'Done!'
s.quit()
