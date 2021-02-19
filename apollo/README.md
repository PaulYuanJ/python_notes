# Apollo Client

Demo.py中举例了如何操作一个namespace下的items
```
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

```

由于该项目是为了监控系统而开发的，所以如果使用apollo存储配置时的value是这种形式：
```
{
    "labels": {
        "host_ip": "1.7.0.25",
        "host_name": "worknode111.cn.prod",
        "application_notes": "prometheus server",
        "application_support": "Paul",
        "location": "Tianjin",
        "platform_support": "CN Linux",
        "node_type": "monitoring_platform",
        "node_role": "Paul_Test_server"
    },
    "targets": [
        "1.7.0.25:9100"
    ]
}
```
可以使用一下方式将配置导出到excel中（由于我们当前监控系统的单个namespace配置条目超过2000，apollo自带的搜索功能只能根据key进行索引，所以开发此功能以便根据labels进行索引）
```
from ApolloTools import ApolloClient

ac_info = {
    'appId': 'NON1001',
    'clusterName': 'defect',
    'namespaceName': 'application',
}
# the name of the excel will be like this: {appId}_{clusterName}_{namespaceName}.xlsx
ac.dump_to_excel()
```