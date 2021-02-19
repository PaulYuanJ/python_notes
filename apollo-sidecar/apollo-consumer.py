#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: apollo-comsumer.py
@created_time: 2/9/2021 11:01 AM
@updated_time:
@desc: Just for fun :)
'''

from flask import Flask, request, jsonify
import json
import os
import datetime

app = Flask(__name__)


def backup_file(filename, content, amount=5):
    path, file = os.path.split(filename)
    path = '.' if path == '' else path
    if os.path.exists(filename):
        os.rename(filename, f'{filename}_{datetime.datetime.now().strftime("%F_%H%M%S")}')
    files =[_file for _file in os.listdir(f'{path}/') if _file.startswith(f'{file}_') == True][::-1]

    if len(files) >= amount:
        deleted_files = files[amount:]

        [os.remove(f'{path}/{file}') for file in deleted_files]
    with open(filename, 'w') as fp:
        fp.write(json.dumps(json.loads(content), indent=4, separators=(',', ': ')))


@app.route('/consumer', methods=["POST", "GET"])
def get_metrics():
    if request.method == "POST":
        try:
            data = json.loads(request.get_data(as_text=True))
            filename = data.get('filename')
            content = data.get('file_content')
            backup_file(filename, content)
            return jsonify({'status': 'ok'})
        except Exception as e:
            print(json.loads(request.get_data(as_text=True)))
            return jsonify({'status': 'nok', 'message': f'{e}'})
    else:
        return jsonify({'status': 'nok', 'message': 'please use POST method'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=9898, debug=True)