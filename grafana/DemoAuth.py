#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: DemoAuth.py
@created_time: 3/29/2021 12:21 PM
@updated_time: 
@desc: Just for fun :)
'''


from grafana_api.grafana_face import GrafanaFace
from urllib.parse import urlparse

def login_grafana(url, username, password) -> GrafanaFace:
    parser = urlparse(url)
    auth = GrafanaFace(
        auth=(username, password),
        # 如果是用api key, 则为auth="api key"
        host=parser.netloc,
        verify=False,
        protocol=parser.scheme,
        timeout=15
    )
    return auth

if __name__ == '__main__':
    domain = "https://monitoring.uat.XXXX.cn"
    username = ""
    password = ""
    auth = login_grafana(domain, username, password)
    orgs = auth.organizations.list_organization()
    orgs_length = len(orgs)
    print(orgs_length)