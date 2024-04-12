from django.contrib import admin
from . models import *
from auth_app.models import Class, Student, AttendanceRecord, Teacher

# Register your models here.
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(AttendanceRecord)
admin.site.register(Teacher)
