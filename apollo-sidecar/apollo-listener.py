#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: Notifier.py
@created_time: 2/5/2021 11:20 AM
@updated_time:
@desc: Just for fun :)
'''

import pandas as pd
from sqlalchemy import create_engine
import yaml
import os
import time
import json
import requests
from prometheus_client import Gauge, start_http_server, Counter


pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

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
        return create_engine(
            'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=%(charset)s' %
            mysql_config,
            encoding='utf-8')

    def query(self, sql_list):
        if not isinstance(sql_list, list):
            sql_list = [sql_list]
        for sql in sql_list:
            yield pd.read_sql(sql, con=self.engine)


    def send2webhook(self, released_configuration):
        '''
        :param released_configuration:
        {
            'AppId': 'NON1001',
            'ClusterName': 'default',
            'NamespaceName': 'application',
            'Configurations': ''
        }
        :return:
        '''
        webhooks = self.config_dict.get('receiver')
        appid = released_configuration.get("AppId")
        cluster = released_configuration.get("ClusterName")
        namespace = released_configuration.get("NamespaceName")

        for webhook in webhooks:

            if len(webhook.get('match') & released_configuration.items()) == 3:
                print(f'{webhook.get("match").items()}, '
                      f'Send to Webhook {webhook.get("web_hook")}')
                for hook in webhook.get("web_hook"):
                    url = hook.get('url')
                    filename = hook.get('target')
                    configuration_content = json.loads(released_configuration.get('Configurations'))
                    file_content = json.dumps([json.loads(c) for c in configuration_content.values()])

                    data = {
                        'filename': filename,
                        'file_content': file_content
                    }
                    print(appid, cluster, namespace)
                    try:
                        response = requests.request(
                            url=url,
                            method='POST',
                            data=json.dumps(data)
                        )
                        result = response.json()
                        if result.get('status') == 'ok':
                            prometheus_metric_sendwehook_s.labels(
                                appid=appid,
                                cluster=cluster,
                                namespace=namespace).inc()
                        else:
                            prometheus_metric_sendwehook_f.labels(
                                appid=appid,
                                cluster=cluster,
                                namespace=namespace).inc()
                    except Exception as e:
                        print(e)
                        prometheus_metric_sendwehook_f.labels(
                            appid=appid,
                            cluster=cluster,
                            namespace=namespace).inc()
            break
        else:
            prometheus_metric_sendwehook_o.labels(
                    appid=appid,
                    cluster=cluster,
                    namespace=namespace).inc()
if __name__ == '__main__':

    prometheus_metric_sendwehook_s = Counter('apollo_listener_sendwehook_s', 'succeed',
                                         ['appid', 'cluster', 'namespace'])
    prometheus_metric_sendwehook_f = Counter('apollo_listener_sendwehook_f', 'failed',
                                         ['appid', 'cluster', 'namespace'])
    prometheus_metric_sendwehook_o = Counter('apollo_listener_sendwehook_o', 'other',
                                         ['appid', 'cluster', 'namespace'])

    start_http_server(10010)
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
                            mc.query(f'select AppId,ClusterName,NamespaceName,Configurations '
                                     f'from ApolloConfigDB.Release '
                                     f'where ApolloConfigDB.Release.id > {cache};'):
                        for i, configuration in result.iterrows():
                            mc.send2webhook(configuration.to_dict())
                else:
                    print(f'Started the apollo-listener...')


            cache = release_count

        except Exception as e:
            print(e)
            mc.__init__('conf/config.yaml')

        time.sleep(5)
