from rest_framework import serializers
from .models import Employee, Department, Projects

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'salary', 'designation', 'address', 'department']  

class ProjectSerializer(serializers.ModelSerializer):
    team = EmployeeSerializer(many=True, read_only=True)
    class Meta:
        model = Projects
        fields = ['id', 'name', 'team_lead', 'status', 'start_date', 'end_date', 'team']
