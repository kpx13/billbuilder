# -*- coding: utf-8 -*-

import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
    

def send_mail_by_queue(email, subject, body, files=[]):
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=json.dumps({ 'action': 'send_mail',
                                            'msg': {
                                                        'email': email,
                                                        'subject': subject,
                                                        'body': body,
                                                        'files': files,
                                                    }}))