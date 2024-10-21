from datetime import date
from os import stat
from django.http import JsonResponse
from django.shortcuts import render,redirect
from requests import Response
from django.db.models import Sum
from crudapp.models import Employee,Department, Projects
from crudapp.serializers import  DepartmentSerializer, EmployeeSerializer, ProjectSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response as R
class EmployeeDetails(APIView):
    def get(self,request):
        obj = Employee.objects.all()
        serializer = EmployeeSerializer(obj,many = True)
        return R(data=serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return R(data=serializer.data,status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return R(data=serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeDepartmentInfo(APIView):
    def get(self,request,fid):
        try:
            obj = Employee.objects.get(id=fid)

        except Employee.DoesNotExist:
            msg = {"msg":"not found"}
            return R(msg,status=status.HTTP_404_NOT_FOUND)
        
        department_name = obj.department.dname if obj.department else "No department assigned"
        return R(department_name,status=status.HTTP_200_OK)
    
class EmployeeInfo(APIView):
    def get(self,request,fid):
        try:
            obj = Employee.objects.get(id=fid)

        except Employee.DoesNotExist:
            msg = {"msg":"not found"}
            return R(msg,status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(obj)
        return R(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,fid):
        try:
            obj = Employee.objects.get(id=fid)
        except Employee.DoesNotExist:
             msg = {"msg":"not found"}
             return R(msg,status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(obj,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return R(serializer.data,status=status.HTTP_205_RESET_CONTENT)
        
        return R(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,fid):
        try:
            obj = Employee.objects.get(id=fid)
        except Employee.DoesNotExist:
            msg = {"msg":"not found"}
            return R(msg,status=status.HTTP_404_NOT_FOUND)
        
        obj.delete()
        return R({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)

class DepartmentDetails(APIView):
    def get(self,request):
        obj = Department.objects.all()
        serializer = DepartmentSerializer(obj,many = True)
        return R(data=serializer.data,status=status.HTTP_200_OK)
    

    def post(self,request):
        serializer = DepartmentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return R(data=serializer.data,status=status.HTTP_201_CREATED)
        return R(data=serializer.data,status=status.HTTP_400_BAD_REQUEST)
    

class DepartmentInfo(APIView):
    def get(self,request,fid):
        try:
            obj = Department.objects.get(id=fid)

        except Department.DoesNotExist:
            msg = {"msg":"not found"}
            return R(msg,status=status.HTTP_404_NOT_FOUND)
        
        serializer = DepartmentSerializer(obj)
        return R(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,fid):
        try:
            obj = Department.objects.get(id=fid)
        except Department.DoesNotExist:
             msg = {"msg":"not found"}
             return R(msg,status=status.HTTP_404_NOT_FOUND)
        
        serializer = DepartmentSerializer(obj,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return R(serializer.data,status=status.HTTP_205_RESET_CONTENT)
        
        return R(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,fid):
        try:
            obj = Department.objects.get(id=fid)
        except Department.DoesNotExist:
            msg = {"msg":"not found"}
            return R(msg,status=status.HTTP_404_NOT_FOUND)
        
        
        obj.delete()
        return R({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)

class ProjectInfo(APIView):
    def get(self,request):
        obj = Projects.objects.all()
        serializer = ProjectSerializer(obj,many = True)
        return R(data=serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = ProjectSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return R(data=serializer.data,status=status.HTTP_201_CREATED)
        return R(data=serializer.data,status=status.HTTP_400_BAD_REQUEST)

class ProjectDetails(APIView):
    def get(self,request,fid):
        try:
            obj = Projects.objects.get(id=fid)
        except Projects.DoesNotExist:
            msg = {'msg' : 'Not found'}
            return R(msg,status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectSerializer(obj)
        return R(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request,fid):
        try:
            obj = Projects.objects.get(id=fid)
        except Projects.DoesNotExist:
            msg = {"msg":"not found"}
            return R(msg,status=status.HTTP_404_NOT_FOUND)
        
        if obj.end_date < date.today():
            obj.delete()
            return R({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)
    
        return R({'msg':'Cant Delete a Ongoing Project'},status=status.HTTP_404_NOT_FOUND)


class AddMember(APIView):
    def put(self, request, fid):
        try:
            project = Projects.objects.get(id=fid)
        except Projects.DoesNotExist:
            return R({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        member_id = request.data.get('member_id')

        if member_id is not None:
            try:
                employee = Employee.objects.get(id=member_id)
                project.team.add(employee)
                project.save()
                return R({'message':'Member Added'},status=status.HTTP_202_ACCEPTED)
            
            except employee.DoesNotExist:
                return R({'message':'Not Found'},status=status.HTTP_404_NOT_FOUND)
            
        return R({'message':'Please enter valid member id'})

class UpdateStatus(APIView):
    def put(self, request, fid):
        try:
            project = Projects.objects.get(id=fid)
        except Projects.DoesNotExist:
            return R({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        n_status = request.data.get('status')

        if n_status is not None:
            if n_status in dict(Projects.STATUS_CHOICES):
                try:
                    project.status = n_status
                    project.save()
                    return R({'message':'Status Updated'},status=status.HTTP_202_ACCEPTED)
            
                except Projects.DoesNotExist:
                    return R({'message':'Not Found'},status=status.HTTP_404_NOT_FOUND)
            
        return R({'message':'Please enter valid status'})
    
class Newproject(APIView):
    def get(self,request):
        try:
            new = Projects.objects.all()
        
        except Projects.DoesNotExist:
            return R({"error": "No New Project found."}, status=status.HTTP_404_NOT_FOUND)
    
        projects = [project for project in new if project.status in ['New', 'NEW']]

        if not projects:
            return R({'message':'New Projects Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(projects,many =True)
        return R(data=serializer.data,status=status.HTTP_302_FOUND)
    
class Ongoing_project(APIView):
    def get(self,request):
        try:
            new = Projects.objects.all()
        
        except Projects.DoesNotExist:
            return R({"error": "No New Project found."}, status=status.HTTP_404_NOT_FOUND)
    
        projects = [project for project in new if project.status in ['ON-GOING', 'On-going']]

        if not projects:
            return R({'message':'New Projects Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(projects,many =True)
        return R(data=serializer.data,status=status.HTTP_302_FOUND)
    
class Endedproject(APIView):
    def get(self,request):
        try:
            new = Projects.objects.all()
        
        except Projects.DoesNotExist:
            return R({"error": "No New Project found."}, status=status.HTTP_404_NOT_FOUND)
    
        projects = [project for project in new if project.status in ['ENDED', 'Ended']]

        if not projects:
            return R({'message':'New Projects Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(projects,many =True)
        return R(data=serializer.data,status=status.HTTP_302_FOUND)



class Budget(APIView):
    def get(self,request,fid):
        try:
            project = Projects.objects.get(id=fid)
            # employee = Employee.objects.all()
        except Projects.DoesNotExist:
            return R({"error": "No Project found."}, status=status.HTTP_404_NOT_FOUND)
        budget = 0
        team = project.team.all()
        for i in team:
            budget += i.salary
        
        extra_budget = 20000
        budget += extra_budget
        return R({'project_id': project.id, 'total_budget': budget}, status=status.HTTP_200_OK)

class Highest_salary(APIView):
    def get(self,request):
        employees = Employee.objects.all()
        highest = max(employee.salary for employee in employees)
        return R({'highest salary': highest}, status=status.HTTP_200_OK)

class Second_highest(APIView):
    def get(self,request):
        employees = Employee.objects.all()
        set_salary = sorted(set(employee.salary for employee in employees), reverse=True)
        second_highest = set_salary[1]
        return R({'second highest salary': second_highest}, status=status.HTTP_200_OK)

class SalaryDep(APIView):
    def get(self,request):
        departments = Department.objects.annotate(total_salary=Sum('employee__salary'))
        total_salaries = [
            {
                'department_name': department.dname,
                'total_salary': department.total_salary if department.total_salary else 0
            }
            for department in departments
        ]
        return R(total_salaries, status=status.HTTP_200_OK)