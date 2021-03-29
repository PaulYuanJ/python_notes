#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: grafana_backup.py
@created_time: 3/29/2021 12:20 PM
@updated_time: 
@desc: Just for fun :)
'''

from grafana_api import GrafanaFace
import re
import os
import json
import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_DIR = '/opt/grafana_backup/'
DASHBOARD_BACKUP_DIR = f'{DEFAULT_DIR}backup_dashboards'
CHANNEL_BACKUP_DIR = f'{DEFAULT_DIR}backup_channel'
ORG_BACKUP_DIR = f'{DEFAULT_DIR}backup_org'

'''
curl -H "Authorization: Bearer XXXX" http://monitoring.uat.XXX.cn/api/dashboards/home
'''

API_KEI_LIST = [
    {'XXXXR':
         {'name':'Main Org.', 'id':'1'}},
    {'XXXXF':
         {'name':'Business', 'id':'2'}}
]

def export_dashboards():
    for i in API_KEI_LIST:
        auth = GrafanaFace(
            auth=tuple(i.keys())[0],
            host='monitoring.homecreditcfc.cn',
            protocol='https',
            verify=False
        )
        auth.api.timeout = 60
        org = auth.organization.get_current_organization()
        folders = auth.folder.get_all_folders()
        backup_dir = DASHBOARD_BACKUP_DIR
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)
        org_dir = org.get('name')
        if not os.path.exists(f'{backup_dir}/{org_dir}'):
            os.mkdir(f'{backup_dir}/{org_dir}')
        folders_len = len(folders)
        for i_folder, folder in enumerate(folders):
            if True:
                folder_title = '_'.join(re.findall('[a-zA-Z0-9]+', folder.get('title'), re.S) )
                if not os.path.exists(f'{backup_dir}/{org_dir}/{folder_title}'):
                    os.mkdir(f'{backup_dir}/{org_dir}/{folder_title}')
                folder_id = folder.get('id')
                dashboards = auth.search.search_dashboards(folder_ids=folder_id, query=None)
                dashboards_len = len(dashboards)
                for i_dashboard, dashboard in enumerate(dashboards):
                    try:
                        _json = auth.dashboard.get_dashboard(dashboard.get('uid'))
                        dashboard_name = _json.get('meta').get('slug')
                        with open(f'{backup_dir}/{org_dir}/{folder_title}/{dashboard_name}.json', 'w') as fp:
                            fp.write(json.dumps(_json.get('dashboard')))
                            print(f'{org.get("name")}, Folders:[{i_folder + 1}/{folders_len}], Dashboards:[{i_dashboard + 1}/{dashboards_len}]')

                    except Exception as e:
                        print(e)

def export_channel():
    for i in API_KEI_LIST:
        auth = GrafanaFace(
            auth=tuple(i.keys())[0],
            host='monitoring.homecreditcfc.cn',
            protocol='https',
            verify=False
        )
        backup_dir = CHANNEL_BACKUP_DIR
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)
        org = auth.organization.get_current_organization()
        org_dir = org.get('name')
        if not os.path.exists(f'{backup_dir}/{org_dir}'):
            os.mkdir(f'{backup_dir}/{org_dir}')

        channels = auth.notifications.get_channels()
        channels_len = len(channels)
        for i_channel, channel in enumerate(channels):
            channel_uid = channel.get('uid')
            channel_name = channel.get('name')
            _json = auth.notifications.get_channel_by_uid(channel_uid)
            with open(f'{backup_dir}/{org_dir}/{channel_name}.json', 'w') as fp:
                fp.write(json.dumps(_json))
                print(f'{org.get("name")}, Channels:[{i_channel + 1}/{channels_len}]')

def export_org():
    for i in API_KEI_LIST:
        auth = GrafanaFace(
            auth=tuple(i.keys())[0],
            host='monitoring.homecreditcfc.cn',
            protocol='https',
            verify=False
        )

        org = auth.organization.get_current_organization()
        users = auth.organization.get_current_organization_users()
        backup_dir = ORG_BACKUP_DIR
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)
        org_dir = org.get('name')
        if not os.path.exists(f'{backup_dir}/{org_dir}'):
            os.mkdir(f'{backup_dir}/{org_dir}')
        with open(f'{backup_dir}/{org_dir}.json', 'w') as fp:
            fp.write(json.dumps(org))
        user_len = len(users)
        for i_user, user in enumerate(users):
            user_name = user.get('name')
            with open(f'{backup_dir}/{org_dir}/user_{user_name}.json', 'w') as fp:
                fp.write(json.dumps(user))
                print(f'{org.get("name")}, User:[{i_user + 1}/{user_len}]')

def export_all():
    export_dashboards()
    export_channel()
    export_org()
    with open(f'{DEFAULT_DIR}FinishedTime', 'w') as fp:
        fp.write(f'{datetime.datetime.now()}')

if __name__ == '__main__':
    export_all()
