from django.db import models
from django.utils import timezone

# Create your models here.

class Employee(models.Model):

    name = models.CharField(max_length=128, default="demo")
    create_datetime = models.DateTimeField(null=True, default=timezone.now)
    create_author = models.CharField(max_length=64, default="demo")
    update_datetime = models.DateTimeField(auto_now=True, null=True)
    update_author = models.CharField(max_length=64, default="demo")
    is_oncall = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

class Department(models.Model):

    name = models.CharField(max_length=128, default="demo")
    create_datetime = models.DateTimeField(null=True, default=timezone.now)
    create_author = models.CharField(max_length=64, default="demo")
    update_datetime = models.DateTimeField(auto_now=True, null=True)
    update_author = models.CharField(max_length=64, default="demo")
    employee = models.ManyToManyField(Employee, through='Employee_Department')

    def employee_list(self, name=None):
        final_list = []

        if name == None:
            for i in self.employee.all():
                _employee = Employee.objects.filter(name=f'{i}').all()
                for rr in _employee:
                    final_list.append(rr.__dict__)
        else:
            for i in name:
                _employee = Employee.objects.filter(name=f'{i}').all()
                for rr in _employee:
                    final_list.append(rr.__dict__)
        return final_list

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'


class Employee_Department(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = "employee_department_relationship"
        unique_together = [
            ('employee', 'department')
        ]