from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=100, default='unknown')
    LastName = models.CharField(max_length=100, default='Unknown')
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
    


    #def __str__(self):
    #  return self.name


# Ensure this is only defined once
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    RollNumber = models.BigIntegerField(default=0)
    Degree = models.CharField(max_length=30)
    Major = models.CharField(max_length=64)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# Define AttendanceRecord once
class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    #class_attended = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()  # True for present, False for absent

    #def __str__(self):
        #return f"{self.student} - {self.class_attended} - {self.date}: {'Present' if self.status else 'Absent'}"


class Class(models.Model):
    name = models.CharField(max_length=100)
    
    
class Semester(models.Model):
    name = models.CharField(max_length=100)