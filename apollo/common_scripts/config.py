#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: config.py
@created_time: 8/4/2020 8:35 AM
@updated_time:
@desc: Just for fun :)
'''

class Configurer(object):

    __TOKEN = {

        1001: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        1002: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        2001: ' XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ',
        "NON1001": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }


    def _token(self, appId):
        try:
            return self.__TOKEN.get(int(appId))
        except:
            return self.__TOKEN.get(appId)

    @property
    def apollo_url(self):
        protocol = 'https'
        domain = 'apollo.prod.cn'
        return f'{protocol}://{domain}'

