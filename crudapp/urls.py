from . import views
from django.contrib import admin
from django.urls import path
from .views import AddMember, Budget, DepartmentDetails, DepartmentInfo, EmployeeDepartmentInfo, EmployeeDetails, EmployeeInfo, Endedproject, Highest_salary, Newproject, Ongoing_project, ProjectDetails, ProjectInfo, SalaryDep, Second_highest, UpdateStatus

urlpatterns = [
    path('employees/',EmployeeDetails.as_view(),name= 'employees'),
    path('employees/<int:fid>/departments/',EmployeeDepartmentInfo.as_view(),name= 'employeedepartment'),
    path('employees/<int:fid>/',EmployeeInfo.as_view()),
    path('departments/',DepartmentDetails.as_view(),name= 'departments'),
    path('departments/<int:fid>/',DepartmentInfo.as_view()),
    path('projects/',ProjectInfo.as_view()),
    path('projects/<int:fid>/',ProjectDetails.as_view()),
    path('projects/<int:fid>/add-member/',AddMember.as_view()),
    path('projects/<int:fid>/',ProjectDetails.as_view()),
    path('projects/<int:fid>/update-status/',UpdateStatus.as_view()),
    path('projects/new/',Newproject.as_view()),
    path('projects/on-going/',Ongoing_project.as_view()),
    path('projects/ended/',Endedproject.as_view()),
    path('projects/<int:fid>/budget/',Budget.as_view()),
    path('employees/highest-salary/',Highest_salary.as_view()),
    path('employees/second-highest-salary/',Second_highest.as_view()),
    path('departments/total-salary/',SalaryDep.as_view()),


]
