#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: PrometheusQueryClient.py
@created_time: 2/3/2021 11:06 PM
@updated_time: 
@desc: Just for fun :)
'''


import requests
import json

class PrometheusQueryAgent(object):
    def __init__(self, prometheus_url):
        self.prometheus_url = prometheus_url

    def prometheus_query(self, metric, _time="") -> dict:
        try:

            uri = '/api/v1/query'

            params = {
                'query': metric,
                'time': _time
            }

            return requests.request(
                method="GET",
                url=f'{self.prometheus_url.strip("/")}{uri}',
                verify=False,
                params=params
            ).json()
        except Exception as e:
            return {'exception': e}

    def prometheus_query_range(self, metric, start="", end="", step="15s"):
        try:

            uri = '/api/v1/query_range'

            params = {
                'query': metric,
                'start': start,
                'end': end,
                'step': step
            }

            return requests.request(
                method="GET",
                url=f'{self.prometheus_url.strip("/")}{uri}',
                verify=False,
                params=params
            ).json()
        except Exception as e:
            return {'exception': e}


if __name__ == '__main__':
    pqa = PrometheusQueryAgent("http://192.168.56.102:30090/")
    result_query = pqa.prometheus_query(metric='up')
    print(result_query)

    time_start = '2021-02-03T13:26:58.261Z'
    time_end = '2021-02-03T14:26:58.261Z'
    result_query_range = pqa.prometheus_query_range(metric='up',
                                                    start=time_start,
                                                    end=time_end)
    print(result_query_range)