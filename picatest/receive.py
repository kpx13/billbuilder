#!/usr/bin/env python
import pika
import json
import smtplib
from email.mime.text import MIMEText

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

def callback(ch, method, properties, body):
    print " [x] Received"
    event = json.loads(body)
    if event['action'] == 'send_mail':
        send_mail(event['msg']['email'], event['msg']['subject'], event['msg']['body'])
        print 'MAIL SENT to %s' % event['msg']['email'] 
        
    
channel.basic_consume(callback, queue='hello', no_ack=True)
channel.start_consuming()