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
import  time

class MsgProducer(object):
    def __init__(self):
        # 制作一个鉴权消息
        credentials = pika.PlainCredentials("admin", "1111qqqq")
        # 初始化一个长连接
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.56.103', port=5672, credentials=credentials))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='broadcast', exchange_type='fanout')

    def publish_msg(self, msg_body):
        self.channel.basic_publish(exchange='broadcast',
                                   routing_key='',
                                   body=f'{msg_body}!')
        print(f" [x] Sent '{msg_body}!'")

    def __repr__(self):
        return f"class {self.__class__.__name__}" \
            f" will simulate message producer."

    def main_loop(self):
        message_body = "Hello RabbitMQ"
        i = 0
        try:
            while True:
                self.publish_msg(f"[{i}]{message_body}")
                time.sleep(3)
                i += 1
        except KeyboardInterrupt:
            self.connection.close()

if __name__ == '__main__':
    a = MsgProducer()
    a.main_loop()