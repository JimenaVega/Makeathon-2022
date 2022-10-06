import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

gmail_user = 'fire.detector.pycom@gmail.com'
gmail_pwd = 'tnzdkbsqeiwgmuep'
TO = "nachofnz22@gmail.com"
SUBJECT = "FIRE ALERT"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_user, gmail_pwd)


msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = gmail_user
msg['To'] = TO
with open('fireAlert.html', 'r') as f:
    BODY = MIMEText(f.read(), 'html')
    msg.attach(BODY)
    server.sendmail(gmail_user, [TO], msg.as_string())
    print('email sent')
