#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: KubeClient.py
@created_time: 1/18/2021 7:54 AM
@updated_time:
@desc: Just for fun :)
'''

from kubernetes import client, config
import os

class KubectlAgent(object):
    def __init__(self, auth_file):
        if not os.path.exists(auth_file):
            print(f'could not find auth file {auth_file}')
            exit(-1)
        config.kube_config.load_kube_config(config_file=auth_file)
        config.kube_config.Configuration.verify_ssl = False

    def kubectl_get_node_by_name(self, node_name:str, without=False):
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        if without == False:
            return [node for node in nodes.items if node.metadata.name == node_name]
        else:
            return [node for node in nodes.items if node.metadata.name != node_name]

    def kubectl_get_node_by_label(self, label_dict:dict, without=False):
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        if without == False:
            return [node for node in nodes.items
                        for label_key, label_value in node.metadata.labels.items()
                    if label_dict.get(label_key) == label_value]
        else:
            return [node for node in nodes.items
                        for label_key, label_value in node.metadata.labels
                    if label_dict.get(label_key) != label_value]

    def kubectl_get_node_by_annotation(self, annotation_dict:dict, without=False):
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        if without == False:
            return [node for node in nodes.items
                        for annotation_key, annotation_value in node.metadata.annotations.items()
                        if annotation_dict.get(annotation_key) == annotation_value]
        else:
            return [node for node in nodes.items
                        for annotation_key, annotation_value in node.metadata.annotations
                        if annotation_dict.get(annotation_key) != annotation_value]

    def kubectl_get_node_by_unschedulable(self, unschedulable:bool):
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        return [node.metadata.name for node in nodes.items
                if node.spec.unschedulable == unschedulable]

    def kubectl_annotate_node(self, node_name, annotation:dict):
        v1 = client.CoreV1Api()
        body = {
            "metadata": {
                "annotations": annotation
            }
        }
        result = v1.patch_node(node_name, body)
        return result

    def kubectl_unannotate_node(self, node_name, annotation:dict):
        v1 = client.CoreV1Api()
        nodes = self.kubectl_get_node_by_name(node_name)
        if len(nodes) >= 1:
            node = list(nodes)[0]
            for key, value in annotation.items():
                node.metadata.annotations[key] = None
            print(v1.patch_node(node_name, body=node))
        else:
            print(f"could not find the node {node_name}")

    def kubectl_cordon_node(self, node_name):
        v1 = client.CoreV1Api()

        body = {
            "spec": {
                "unschedulable": True
            }
        }
        v1.patch_node(node_name, body)

    def kubectl_uncordon_node(self, node_name):
        v1 = client.CoreV1Api()

        body = {
            "spec": {
                "unschedulable": False
            }
        }
        v1.patch_node(node_name, body)

