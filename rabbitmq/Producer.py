#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: Producer.py
@created_time: 1/22/2021 10:22 PM
@updated_time: 
@desc: Just for fun :)
'''

import pika

class MsgProducer(object):
    def __init__(self):
        # 制作一个鉴权消息
        credentials = pika.PlainCredentials("admin", "1111qqqq")
        # 初始化一个长连接
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.56.103', port=5672, credentials=credentials))

        self.channel = self.connection.channel()

    def publish_msg(self, queue_name, msg_body):
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   body=f'{msg_body}!')
        print(f" [x] Sent '{msg_body}!'")

    def __repr__(self):
        return f"class {self.__class__.__name__}" \
            f" will simulate message producer."

    def main_loop(self):
        queue_name = 'my_first_queue'
        message_body = "Hello RabbitMQ"
        self.channel.queue_declare(queue=queue_name)
        self.publish_msg(queue_name, message_body)
        self.connection.close()

if __name__ == '__main__':
    a = MsgProducer()
    a.main_loop()