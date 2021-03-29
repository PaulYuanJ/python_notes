#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: apollo-mysql-pandas.py
@created_time: 2/4/2021 1:00 PM
@updated_time: 
@desc: Just for fun :)
'''

import pandas as pd
from sqlalchemy import create_engine
import yaml
import os
import time

class MysqlClient(object):

    def __init__(self, config_file):
        self.config_dict = self.parse_config(config_file)
        self.apollo_config = self.config_dict.get('apollo')
        self.mysql_config = self.config_dict.get('mysql')
        self.engine = self.init_mysql_session(self.mysql_config)

    def parse_config(self, filename) -> dict:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as fp:
                config_dict = yaml.safe_load(fp)
                return config_dict
        else:
            exit(-1)

    def init_mysql_session(self, mysql_config):
        return create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=%(charset)s' %
                             mysql_config,
                             encoding='utf-8')

    def query(self, sql_list):
        if not isinstance(sql_list, list):
            sql_list = [sql_list]
        for sql in sql_list:
            yield pd.read_sql(sql, con=self.engine)

if __name__ == '__main__':
    mc = MysqlClient('conf/config.yaml')
    sql_release_sql = 'select max(id) from ApolloConfigDB.Release;'
    apollo_info_sql = ''

    cache = None

    while True:
        try:

            release_count = next(mc.query(sql_release_sql))['max(id)'][0]

            if cache != release_count:
                if cache != None:
                    for result in \
                            mc.query(f'select AppId,ClusterName,NamespaceName,Configurations from ApolloConfigDB.Release where ApolloConfigDB.Release.id > {cache};'):
                        for row in result.iterrows():

                            print(row[1].to_dict())
                else:
                    print(release_count)
                    print(next(mc.query('desc ApolloConfigDB.Release;')))

            cache = release_count

        except Exception as e:
            mc.__init__('conf/config.yaml')

        time.sleep(5)


