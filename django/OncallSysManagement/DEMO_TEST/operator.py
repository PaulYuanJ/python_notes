#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: operator.py.py
@created_time: 7/20/2021 9:42 AM
@updated_time: 
@desc: Just for fun :)
'''
import requests
import json
from faker import Faker

fake = Faker()

def operator(method, url, data:dict):

    params = data.get("params", "")
    _data = data.get("data", "")

    print(_data)
    response = requests.request(
        method=method,
        url=url,
        params=params,
        data=_data,
        headers={
            'Accept': 'application/json',
            # 'Content-Type': 'application/json'
        }
    ).json()
    print(json.dumps(response, indent=4, separators=(",", ": ")))
    return response

def get_api_root():
    print(" ========== Get API Root ========== ")
    operator("GET", "http://localhost:8080/oncall/", {})

def get_department():
    print(" ========== Get department ========== ")
    operator("GET", "http://127.0.0.1:8080/oncall/department", {})

def get_employee():
    print(" ========== Get employee ========== ")
    operator("GET", "http://127.0.0.1:8080/oncall/employee", {})

def add_employee():
    print(" ========== Add employee ========== ")
    creator = fake.name()
    employee = {
        "data": {
            "name": fake.name(),
            "create_author": creator,
            "update_author": creator,
            "is_oncall": False
        }
    }

    return operator("POST", "http://127.0.0.1:8080/oncall/employee", employee)
