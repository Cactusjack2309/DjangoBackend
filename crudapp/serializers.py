from rest_framework import serializers 
from .models import  Employee,Department, Projects

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'salary', 'department','designation', 'address','project']

class ProjectSerializer(serializers.ModelSerializer):
    team = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        fields = ['id', 'name', 'team', 'team_lead', 'status', 'start_date', 'end_date']

	
class DepartmentSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Department
		fields = "__all__"
