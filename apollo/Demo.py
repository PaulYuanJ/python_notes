#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: Demo.py
@created_time: 2/19/2021 10:15 PM
@updated_time: 
@desc: Just for fun :)
'''

from ApolloTools import ApolloClient

ac_info = {
    'appId': 'NON1001',
    'clusterName': 'defect',
    'namespaceName': 'application',
}

ac = ApolloClient(**ac_info)

# get released configuration according to the ac_info
configurations = ac.get_release_namespace().get('configurations')
print(configurations)

# create new item to the ac_info
new_item = {'new_item_key': 'new_item_value'}
ac.create_item(item=new_item)

# update item in the ac_info
updated_item = {'item_key': 'item_new_value'}
ac.create_item(item=updated_item)

# delete item in the ac_info
ac.delete_item(key='deleted_key')

ac.dump_to_excel()


