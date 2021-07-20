#!/usr/bin/env python
# encoding: utf-8
'''
@author: Paul
@license: (C) Copyright 2018-2020, Paul
@contact: yuanjian0375@163.com
@file: serializers.py.py
@created_time: 7/19/2021 11:15 PM
@updated_time: 
@desc: Just for fun :)
'''

from rest_framework import serializers
from oncall_department.models import *

class EmployeeSerializer(serializers.ModelSerializer):
    create_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"

class TrackEmployeeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)
    class Meta:
        model = Employee
        fields = ('id', 'name')


class DepartmentSerializer(serializers.ModelSerializer):
    create_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    # track fields could be write as this
    # employee = EmployeeSerializer(many=True, read_only=True)
    # employee = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=False,
    #     slug_field='name',
    #     queryset=Employee.objects.all()
    # )
    employee = TrackEmployeeSerializer(many=True)

    class Meta:
        model = Department
        fields = "__all__"

    def create(self, validated_data):

        employee_data = validated_data.pop('employee')

        department = Department.objects.create(**validated_data)
        employees = []  # it will contains list of Building model instance
        for _ in employee_data:
            employee_id = _.pop('id', None)
            employee = Employee.objects.get(id=int(employee_id))
            employees.append(employee)
        department.employee.add(*employees)
        return department

    def update(self, instance, validated_data):

        employee_data = validated_data.pop('employee')

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        employees = []  # it will contains list of Building model instance
        for _ in employee_data:
            employee_id = _.pop('id', None)
            employee = Employee.objects.get(id=int(employee_id))
            employees.append(employee)
        instance.employee.set(employees)
        return instance
