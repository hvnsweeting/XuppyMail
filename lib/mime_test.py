import smtplib

from email.mime.text import MIMEText

filetosend = 'tcp_client.py'
fp = open(filetosend, 'rb')
msg = MIMEText(fp.read())
fp.close()

msg['Subject'] = 'The content of %s' % filetosend
msg['From'] = 'anon@google.com'
msg['To'] = 'famihug@hvn.vn'

s = smtplib.SMTP('localhost')
s.sendmail(msg['From'], [msg['To']], msg.as_string())
print 'Done!'
s.quit()
