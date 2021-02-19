#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: ApolloTools.py
@created_time: 8/4/2020 8:29 AM
@updated_time:
@desc: Just for fun :)
'''
import requests
import json
import datetime
import pandas as pd
from common_scripts.config import Configurer
from common_scripts.DemoLog import Log
import logging
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings()


# logger = Log().getLogger(logfile=f'{__name__}_apollo.log')

class PringLog(object):
    def __init__(self, loglevel:str):
        LOG_FORMAT = "%(asctime)s [%(levelname)s] [line:%(lineno)d] - %(message)s"
        DATE_FORMAT = "%F %T"
        CONSOLE_LOG = logging.StreamHandler()
        logging.basicConfig(level=eval(f"logging.{loglevel.upper()}"), format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[CONSOLE_LOG])
        self.logger =  logging.getLogger()

    def info(self, msg):
        return self.logger.info(msg)

    def debug(self, msg):
        return self.logger.debug(msg)

    def error(self, msg):
        return self.logger.error(msg)

    def warn(self, msg):
        return self.logger.warn(msg)

    def critical(self, msg):
        return self.logger.critical(msg)


class ApolloClient(object):
    def __init__(self, logger=None, logger_level="info", url=None, **kwargs):
        self.cf = Configurer()

        if logger == False:
            self.logger = PringLog(logger_level)
        else:
            _logger = Log()
            self.logger = _logger.getLogger(logfile=f'{__file__}_apollo.log', loglevel=logger_level)

        if url == None:
            self.portal_address = self.cf.apollo_url
        else:
            self.portal_address = url

        if kwargs.get('appId') != None and kwargs.get('clusterName') != None and \
                kwargs.get("namespaceName") != None:
            self.appId = kwargs.get('appId')
            self.clusterName = kwargs.get('clusterName')
            self.namespaceName = kwargs.get('namespaceName')

    def get_clusters_info(self, appId=None):
        if appId == None:
            appId = self.appId
        URL = f'{self.portal_address}/openapi/v1/apps/{appId}/envclusters'
        Method = 'GET'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None
        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header
        ).json()
        self.logger.info(response)
        return response

    def get_cluster(self, appId=None, clusterName=None, env='DEV'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        URL = f'{self.portal_address}/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}'
        Method = 'GET'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None
        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header
        ).json()
        self.logger.info(response)
        return response

    def get_namespace(self, appId=None, clusterName=None, namespaceName=None, env='DEV'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName

        URL = f'{self.portal_address}/openapi/v1/envs/{env}/apps/{appId}' \
            f'/clusters/{clusterName}/namespaces/{namespaceName}'
        Method = 'GET'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None
        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header
        ).json()
        self.logger.info(response)
        return response

    def get_namespace_editor(self, appId=None, clusterName=None, namespaceName=None, env='DEV'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName
        URL = f'{self.portal_address}/openapi/v1/envs/{env}/apps/{appId}' \
            f'/clusters/{clusterName}/namespaces/{namespaceName}/lock'
        Method = 'GET'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None
        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header,
            timeout=15
        ).json()
        self.logger.info(response)
        return response

    def get_item(self, appId=None, clusterName=None, namespaceName=None, key=None, env='DEV'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName
        URL = f'{self.portal_address}/openapi/v1/envs/{env}/apps/{appId}' \
            f'/clusters/{clusterName}/namespaces/{namespaceName}/items/{key}'
        Method = 'GET'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None
        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header
        ).json()
        self.logger.info(response)
        return response

    def get_release_namespace(self, appId=None, clusterName=None, namespaceName=None, env='DEV'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName
        URL = f'{self.portal_address}/openapi/v1/envs/{env}/apps/{appId}' \
            f'/clusters/{clusterName}/namespaces/{namespaceName}/releases/latest'
        Method = 'GET'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None

        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header
        )
        try:
            response = response.json()
            self.logger.info(response)
        except ValueError as e:
            response = response.content.decode('utf-8')
            self.logger.info(response)
            response = None
        return response

    def get_all_items(self, appId=None, clusterName=None, namespaceName=None, env='DEV'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName
        URL = f'{self.portal_address}/openapi/v1/envs/{env}/apps/{appId}' \
            f'/clusters/{clusterName}/namespaces/{namespaceName}'
        Method = 'GET'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None

        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header
        )
        try:
            response = response.json()
        except ValueError as e:
            response = response.content.decode('utf-8')
            self.logger.info(response)
            response = None
        return response

    def create_cluster(self, appId=None, clusterName=None,dataChangeCreatedBy='apollo'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName

        URL = f'{self.portal_address}/openapi/v1/apps/{appId}/clusters'
        Method = 'POST'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None
        payload = {
            'name': clusterName,
            'appId': appId,
            'dataChangeCreatedBy': dataChangeCreatedBy
        }
        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header,
            data=json.dumps(payload)
        ).json()
        self.logger.info(response)
        return response

    def create_namespace(self, appId=None, namespaceName=None, format=None, dataChangeCreatedBy='apollo'):
        if appId == None:
            appId = self.appId
        if namespaceName == None:
            namespaceName = self.namespaceName
        if format not in ['properties', 'xml', 'json', 'yml', 'yaml']:
            self.logger.error(f'format is not supported')
            return None

        URL = f'{self.portal_address}/openapi/v1/apps/{appId}/appnamespaces'
        Method = 'POST'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None
        payload = {
            'name': namespaceName,
            'appId': appId,
            'format': format,
            'isPublic': False,
            'dataChangeCreatedBy': dataChangeCreatedBy
        }
        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header,
            data=json.dumps(payload)
        ).json()
        self.logger.info(response)
        return response

    def create_item(self, appId=None, clusterName=None, namespaceName=None, item=None, env='DEV', dataChangeCreatedBy='apollo'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName
        URL = f'{self.portal_address}/openapi/v1/envs/{env}/apps/{appId}' \
            f'/clusters/{clusterName}/namespaces/{namespaceName}/items'
        Method = 'POST'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None
        payload = {
            'key': tuple(item.keys())[0].strip(' '),
            'value': tuple(item.values())[0],
            'dataChangeCreatedBy': dataChangeCreatedBy,
            'comment': 'register from ApolloTools.py'
        }
        # payload.update(item)
        self.logger.info(payload)
        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header,
            data=json.dumps(payload)
        ).json()
        self.logger.info(response)
        return response

    def update_item(self, appId=None, clusterName=None, namespaceName=None,dataChangeLastModifiedBy='apollo', env='DEV',
                    param=None, comment='', item=None):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName
        URL = f'{self.portal_address}/openapi/v1/envs/{env}/apps/{appId}' \
            f'/clusters/{clusterName}/namespaces/{namespaceName}/items/{tuple(item.keys())[0]}'
        Method = 'PUT'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = param

        payload = {
            'key': tuple(item.keys())[0],
            'value': tuple(item.values())[0],
            'dataChangeLastModifiedBy': dataChangeLastModifiedBy,
            'comment': comment
        }
        self.logger.info(json.dumps(payload))

        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header,
            data=json.dumps(payload)
        )
        try:
            response = response.json()
        except json.decoder.JSONDecodeError as e:
            response = response.content.decode('utf-8')

        self.logger.info(response)
        return response

    def update_text_items(self, appId=None, clusterName=None, namespaceName=None, configText=None, env='DEV'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName
        URL = f'{self.portal_address}/apps/{appId}/envs/{env}/clusters/{clusterName}/namespaces/{namespaceName}/items'
        Method = 'PUT'
        header = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8"
        }
        auth = HTTPBasicAuth("apollo", "admin")
        if configText == None or configText == '' or len(configText.split("\n")) < 1:
            self.logger.critical(f"No configText to update")
            return None

        if namespaceName == "configuration_items_152":
            namespaceId = 367
        elif namespaceName == "configuration_items_153":
            namespaceId = 369
        payload = {'configText': configText, "format": "properties", "namespaceId":namespaceId}
        logging.debug(f'{payload}')
        session = requests.session()
        response = session.request(
            method=Method,
            url=URL, verify=False,
            auth=auth,
            headers=header,
            data=json.dumps(payload)
        )
        # response = session.request('GET', url=f"{self.portal_address}/apps/{appId}"
        # f"/namespaces/{namespaceName}/permissions/ModifyNamespace")
        # response = session.request('GET', url=f"{self.portal_address}/apps/{appId}"
        # f"/namespaces/{namespaceName}/permissions/ReleaseNamespace")
        try:
            response = response.json()
        except json.decoder.JSONDecodeError as e:
            response = response.content.decode('utf-8')

        self.logger.info(response)
        return response


    def delete_item(self, appId=None, clusterName=None, namespaceName=None, key=None, operator='apollo', env='DEV'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName
        if namespaceName.split('.')[-1] in ['xml', 'json', 'yml', 'yaml']:
            key = 'content'

        URL = f'{self.portal_address}/openapi/v1/envs/{env}/apps/{appId}' \
            f'/clusters/{clusterName}/namespaces/{namespaceName}/items/{key}?operator={operator}'
        Method = 'DELETE'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = requests.request(
            method=Method,
            url=URL, verify=False,
            headers=header,
        )
        try:
            response = response.json()
        except json.decoder.JSONDecodeError as e:
            response = response.content.decode('utf-8')

        self.logger.info(response)
        return response

    def release(self, appId=None, clusterName=None, namespaceName=None, releasedBy='apollo', env='DEV'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName
        URL = f'{self.portal_address}/openapi/v1/envs/{env}/apps/{appId}' \
            f'/clusters/{clusterName}/namespaces/{namespaceName}/releases'
        Method = 'POST'
        header = {
            'Authorization': self.cf._token(appId),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        Params = None
        payload = {
            'releaseTitle': f'{datetime.datetime.now().strftime("%F")}',
            'releasedBy': releasedBy,
            'releaseComment': ''
        }

        response = requests.request(
            method=Method,
            url=URL, verify=False,
            params=Params,
            headers=header,
            data=json.dumps(payload)
        )
        try:
            response = response.json()
        except json.decoder.JSONDecodeError as e:
            response = response.content.decode('utf-8')

        self.logger.info(response)
        return response

    def dump_to_excel(self, appId=None, clusterName=None, namespaceName=None, env='DEV'):
        if appId == None:
            appId = self.appId
        if clusterName == None:
            clusterName = self.clusterName
        if namespaceName == None:
            namespaceName = self.namespaceName
        if namespaceName.split('.')[-1] in ['xml', 'json', 'yml', 'yaml']:
            self.logger.error('Only support to dump properties configurations')
            return None
        try:
            configurations = self.get_release_namespace(appId, clusterName, namespaceName, env).get('configurations')
        except Exception as e:
            configurations = None
        if configurations == None:
            self.logger.info('no data to dump')
            return 0
        config_item = []
        columns = None
        for key, value_json in configurations.items():
            format_config = {'key': key}
            value_dict = json.loads(value_json)
            format_config.update({'targets': value_dict.get('targets')})
            format_config.update(value_dict.get('labels'))
            config_item.append(format_config)
            columns = value_dict.keys()
        df = pd.DataFrame(config_item)
        df.to_excel(f'{appId}_{clusterName}_{namespaceName}.xlsx')
        self.logger.info(f'Dumped to {appId}_{clusterName}_{namespaceName}.xlsx')

    def load_from_excel(self, appId=None, clusterName=None, namespaceName=None, env='DEV'):
        pass