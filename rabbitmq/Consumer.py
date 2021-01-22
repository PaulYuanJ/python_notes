#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: Consumer.py
@created_time: 1/22/2021 10:22 PM
@updated_time: 
@desc: Just for fun :)
'''

import pika
import sys,os

class MsgConsumer(object):
    def __init__(self):
        # 制作一个鉴权消息
        credentials = pika.PlainCredentials("admin", "1111qqqq")
        # 初始化一个长连接
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.56.103', port=5672, credentials=credentials))

        self.channel = self.connection.channel()

    def do_something(self, msg):
        print(f"Can handle {msg} here.")

    def consume_msg(self, queue_name):

        def callback(ch, method, properties, body):
            print(" [x] %s Received %r" % (self.__class__.__name__,body))
            self.do_something(body)

        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def __repr__(self):
        return f"class {self.__class__.__name__}" \
            f" will simulate message consumer."

    def main_loop(self):
        queue_name = 'my_first_queue'

        self.channel.queue_declare(queue=queue_name)

        try:
            self.consume_msg(queue_name)
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)


if __name__ == '__main__':
    a = MsgConsumer()
    a.main_loop()

