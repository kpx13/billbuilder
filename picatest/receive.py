#!/usr/bin/env python
import pika
import json

import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

print ' [*] Waiting for messages. To exit press CTRL+C'

def send_mail(email, subject, text):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('noreply@webgenesis.ru', 'noreply13')
    msg = MIMEText(text.encode('utf-8'), 'html')
    msg['Subject'] = subject.encode('utf-8')
    msg['From'] = 'LifeRacing'
    msg['To'] = email
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    
def send_mail_with_attach(email, subject, text, files=[]):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('noreply@webgenesis.ru', 'noreply13')
        
    msg = MIMEMultipart()
    msg['From'] = 'BILLder.ru'
    msg['To'] = email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject.encode('utf-8')

    msg.attach( MIMEText(text.encode('utf-8'), 'html') )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open('../' + f,"rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.close()
    
    

def callback(ch, method, properties, body):
    print " [x] Received"
    event = json.loads(body)
    if event['action'] == 'send_mail':
        if 'files' in event['msg']:
            send_mail_with_attach(event['msg']['email'], event['msg']['subject'], event['msg']['body'], event['msg']['files'])
            print 'MAIL SENT to %s' % event['msg']['email']
        else:
            print 'MAIL NOT SENT to %s' % event['msg']['email']
        
    
channel.basic_consume(callback, queue='hello', no_ack=True)
channel.start_consuming()