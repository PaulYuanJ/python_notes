# Create your views here.
from oncall_department.serializers import *
from oncall_department.models import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.order_by('-id')
    serializer_class = EmployeeSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.order_by('-id')
    serializer_class = DepartmentSerializer
    #
    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #
    #     employee = data.get('employee')
    #     new_employee = []
    #     for _ in employee:
    #         employee_obj = Employee.objects.get(id=int(_.get("id")))
    #         employee_data = TrackEmployeeSerializer(employee_obj).data
    #         new_employee.append(employee_data)
    #     data.update({'employee': new_employee})
    #
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)