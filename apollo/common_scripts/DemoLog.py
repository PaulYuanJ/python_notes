#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: DemoLog.py
@created_time: 12/11/2019 2:51 PM
@updated_time:
@desc: Just for fun :)
'''

import logging
import os
from logging.handlers import TimedRotatingFileHandler
import coloredlogs

# 设置颜色
coloredlogs.DEFAULT_FIELD_STYLES = {'asctime': {'color': 'green'}, 'hostname': {'color': 'magenta'},
                                    'levelname': {'color': 'green', 'bold': True}, 'request_id': {'color': 'yellow'},
                                    'name': {'color': 'blue'}, 'programname': {'color': 'cyan'}, 'filename':{'color': 'blue'},
                                    'threadName': {'color': 'yellow'}}


class Log:
    __instances = {}

    @classmethod
    def getLogger(cls, name=os.path.abspath(__name__), logfile='demo.log', loglevel="INFO"):
        if name not in cls.__instances:  # 日志文件夹路径
            BASE_DIR = '.'
            log_dir = 'logs'
            if not log_dir.startswith('/'): # 日志文件夹
                log_dir = os.path.join(BASE_DIR, log_dir)

            # 递归生成
            if not os.path.isdir(log_dir):
                os.makedirs(log_dir, mode=0o755)

            log_file = os.path.join(log_dir, logfile)
            logger = logging.getLogger(name) # 设置日志格式
            fmt = '%(asctime)s [%(levelname)8s] %(filename)s[line:%(lineno)d] %(message)s'
            formater = logging.Formatter(fmt)

            ch = logging.StreamHandler()
            ch.setLevel(Log.__getLogLevel())
            ch.setFormatter(formater)
            logger.addHandler(ch)

            coloredlogs.install(fmt=fmt, level=Log.__getLogLevel(), logger=logger)

            fh = TimedRotatingFileHandler(log_file, when='M', interval=1, backupCount=7, encoding='utf-8')
            fh.setLevel(eval(f"logging.{loglevel.upper()}"))
            fh.setFormatter(formater)
            logger.setLevel(Log.__getLogLevel())
            logger.addHandler(fh)
            cls.__instances[name] = logger
        return cls.__instances[name]


    @staticmethod  # 设置日志等级
    def __getLogLevel():
        return logging.DEBUG

#
# if __name__ == '__main__':
#     Log.getLogger().error('log测试数据1')
#     Log.getLogger().info('log测试数据2')
#     Log.getLogger().warning('log测试数据3')
#     Log.getLogger().debug('log测试数据4')
