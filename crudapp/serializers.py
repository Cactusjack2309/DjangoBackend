from rest_framework import serializers 
from .models import  Employee,Department, Projects

class EmployeeSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Employee
		fields = "__all__"
	

class DepartmentSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Department
		fields = "__all__"

class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Projects
		fields = "__all__"
	
