from django.db import models

# Create your models here.
class Department(models.Model):
    dname = models.CharField(max_length=20)

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    salary = models.DecimalField(max_length=20,decimal_places=2,max_digits=10)
    designation = models.CharField(max_length=20,default="NA")
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    address = models.CharField(max_length=100,default="NA")
    project = models.ManyToManyField('Projects', related_name= 'team_members',default = [])

class Projects(models.Model):

    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('ON-GOING', 'On-going'),
        ('ENDED', 'Ended'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    team = models.ManyToManyField(Employee,related_name='projects')
    team_lead = models.ForeignKey(Employee,on_delete=models.SET_NULL, null=True, related_name='led_projects')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES) 
    start_date = models.DateField()
    end_date = models.DateField()

