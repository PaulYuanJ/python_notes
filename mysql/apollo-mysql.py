#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: apollo-mysql.py
@created_time: 2/4/2021 11:34 AM
@updated_time: 
@desc: Just for fun :)
'''

import pymysql
import yaml
import os

class MysqlClient(object):

    def __init__(self, config_file):
        self.config_dict = self.parse_config(config_file)
        self.apollo_config = self.config_dict.get('apollo')
        self.mysql_config = self.config_dict.get('mysql')
        self.mysql_conn = self.init_mysql_session(self.mysql_config)
        self.cursor = self.mysql_conn.cursor()

    def parse_config(self, filename) -> dict:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as fp:
                config_dict = yaml.safe_load(fp)
                # print(json.dumps(config_dict, indent=4, separators=(',', ': ')))
                return config_dict
        else:
            exit(-1)

    def init_mysql_session(self, mysql_config) -> pymysql.connections:
        return pymysql.connect(**mysql_config)


    def query(self, sql_list):
        if not isinstance(sql_list, list):
            sql_list = [sql_list]
        for sql in sql_list:
            self.cursor.execute(sql)
            yield self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.mysql_conn.close()

if __name__ == '__main__':
    mc = MysqlClient('conf/config.yaml')
    sql_list = ['show databases']
    for result in mc.query(sql_list):
        print(result)