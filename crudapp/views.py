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

    # def post(self,request):
    #     serializer = EmployeeSerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return R(data=serializer.data,status=status.HTTP_201_CREATED)
    #     print(serializer.errors)
    #     return R(data=serializer.data,status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            project_ids = request.data.get('project', [])
            for project_id in project_ids:
                try:
                    project = Projects.objects.get(id=project_id)
                    project.team.add(employee)
                except Projects.DoesNotExist:
                    return R(data={"error": f"No such project found with that specific ID {project_id}"}, status=status.HTTP_400_BAD_REQUEST)

            return R(data=serializer.data, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return R(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeDepartmentInfo(APIView):
    def get(self,request,fid):
        try:
            obj = Employee.objects.get(id=fid)

        except Employee.DoesNotExist:
            msg = {"msg":"not found"}
            return R(msg,status=status.HTTP_404_NOT_FOUND)
        
        department_name = obj.department.dname if obj.department else "No department is assigned"
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

    # def put(self,request,fid):
    #     try:
    #         obj = Employee.objects.get(id=fid)
    #     except Employee.DoesNotExist:
    #          msg = {"msg":"not found"}
    #          return R(msg,status=status.HTTP_404_NOT_FOUND)
        
    #     serializer = EmployeeSerializer(obj,data=request.data,partial=True)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return R(serializer.data,status=status.HTTP_205_RESET_CONTENT)
        
    #     return R(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return R(data={"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
           
            current_projects = list(employee.project.values_list('id', flat=True))
            updated_employee = serializer.save()

          
            new_project_ids = request.data.get('project', [])


            for project_id in current_projects:
                if project_id not in new_project_ids:
                  
                    try:
                        project = Projects.objects.get(id=project_id)
                        project.team.remove(updated_employee)
                    except Projects.DoesNotExist:
                        continue 

            for project_id in new_project_ids:
                if project_id not in current_projects:
                    try:
                        project = Projects.objects.get(id=project_id)
                        project.team.add(updated_employee)
                    except Projects.DoesNotExist:
                        return R(data={"error": f"No such project found with that ID {project_id}"}, status=status.HTTP_400_BAD_REQUEST)

            return R(data=serializer.data, status=status.HTTP_200_OK)

        print(serializer.errors)
        return R(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_object(self, fid):
        try:
            return Department.objects.get(pk=fid)
        except Department.DoesNotExist:
            raise Exception("Department not found")

    def get(self, request, fid):
        department = self.get_object(fid)  
        employees = department.employee_set.all()  
        department_data = {
            "id": department.id,
            "dname": department.dname,
            "employees": [{"id": emp.id, "first_name": emp.first_name, "salary": emp.salary, "designation": emp.designation} for emp in employees]
        }
        return R(department_data)
    
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

    # def post(self,request):
    #     serializer = ProjectSerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return R(data=serializer.data,status=status.HTTP_201_CREATED)
    #     return R(data=serializer.data,status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        
        if serializer.is_valid():
            project = serializer.save()

            employee_ids = request.data.get('team', [])
            
            invalid_employee_ids = []

           
            for employee_id in employee_ids:
                try:
                    
                    employee = Employee.objects.get(id=employee_id)
                    
                    
                    project.team.add(employee)  
                    
                    
                    employee.project.add(project) 
                    
                except Employee.DoesNotExist:
                    
                    invalid_employee_ids.append(employee_id)

            if invalid_employee_ids:
                return Response(
                    data={"error": f"No such employee(s) found with ID(s): {', '.join(map(str, invalid_employee_ids))}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return R(data=serializer.data, status=status.HTTP_201_CREATED)

        return R(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    def get(self, request):
        try:
            highest_salary_employee = Employee.objects.order_by('-salary').first()
            if highest_salary_employee:
                
                response_data = {
                    'id': highest_salary_employee.id,
                    'first_name': highest_salary_employee.first_name,
                    'salary': highest_salary_employee.salary,
                    
                }
                return R(response_data, status=status.HTTP_200_OK)
            else:
                return R({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return R({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Second_highest(APIView):
    def get(self, request):
        try:
            employees = Employee.objects.all()
            if not employees:
                return Response({'error': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)

          
            unique_salaries = sorted(set(employee.salary for employee in employees), reverse=True)

            if len(unique_salaries) < 2:
                return R({'error': 'Not enough distinct salaries to determine second highest'}, status=status.HTTP_404_NOT_FOUND)

            second_highest_salary = unique_salaries[1]  

            second_highest_employees = Employee.objects.filter(salary=second_highest_salary)

            response_data = {
                'second_highest_salary': second_highest_salary,
                'employees': [
                    {
                        'id': employee.id,
                        'first_name': employee.first_name,
                        'salary': employee.salary,
                    }
                    for employee in second_highest_employees
                ]
            }

            return R(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return R({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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