import smtplib, ssl
gmail_user = 'fire.detector.pycom@gmail.com'
gmail_pwd = 'tnzdkbsqeiwgmuep'
TO = "nachofnz22@gmail.com"
SUBJECT = "FIRE"
TEXT = "Hay un incendio"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_user, gmail_pwd)
BODY = '\r\n'.join(['To: %s' % TO,
        'From: %s' % gmail_user,
        'Subject: %s' % SUBJECT,
        '', TEXT])

server.sendmail(gmail_user, [TO], BODY)
print ('email sent')