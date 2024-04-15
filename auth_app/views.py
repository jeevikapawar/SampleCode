import logging
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .middlewares import auth, guest
from django.contrib import messages
from django import forms
from .models import Class
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher, AttendanceRecord, Semester, Class
from .forms import SemesterForm, ClassForm, StudentRegistrationForm

# Create your views here.

def my_view(request):
    try:
        Student = Student.objects.get(user=request.user)
        return HttpResponse("User is a student")
    # User is a student
    except Student.DoesNotExist:
        try:
            Teacher = Teacher.objects.get(user=request.user)
            return HttpResponse("User is a teacher")
        # User is a teacher
        except Teacher.DoesNotExist:
            return HttpResponse("User is neither a student nor a teacher")




def clean_username(self):
    username = self.cleaned_data['username']
    # Check if username is unique
    if User.objects.filter(username=username).exists():
        raise forms.ValidationError("This username is already taken.")
        return username
    
# Your views can then use this form for registration or other purposes

def index_view(request):
    return render(request, 'auth/index.html')

@guest
def register_student(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        

        user_info = User.objects.create_user(username=username, password=password, email=email)
        user_info.save()
        
        student = Student(user=user_info, first_name=first_name, last_name=last_name)
        student.save()

        login(request, user_info)
        return redirect('student_dashboard')
    
    else:

        return render(request, 'auth/student_register.html')

#TEACHER REGISTRATION PAGE
@guest
def register_teacher(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        class_name = request.POST['class_name']

        user = User.objects.create_superuser(username=username, password=password, email=email)
        Teacher.objects.create(user=user, first_name=first_name, last_name=last_name, class_name=class_name)

        login(request, user)
        return redirect('teacher_dashboard')

    return render(request, 'auth/teacher_register.html')

@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            #user = form.get_user()
            if user is not None:
                print("user: is authenticated")
                print("user: is_authenticated", user.is_authenticated)
                login(request,user)
                if not user.is_superuser:
                    print("I'm Student: ",user.get_username)
                    return redirect('student_dashboard')
                else:
                    print("I'm Teacher: ",user.get_username)
                    return redirect('teacher_dashboard')
            # login(request,user)
            else:
                print("user: is not authenticated")

    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

#def dummy_view(request):
    return HttpResponse("<H1>user<H1>")

#creating separate dashboards for students and teachers.
@auth
def student_dashboard(request):

    student_info = Student.objects.get(user=request.user)
    print("Student:", student_info)
    semesters = Semester.objects.all()
    classes = Class.objects.all()
    print("student dashboard")
    attendance_records = AttendanceRecord.objects.filter(student=student_info)
    logger = logging.getLogger(__name__)
    logger.debug("Entering student_dashboard view")
    print("PRint something")
    if not request.user.is_authenticated:
        logger.warning("User not authenticated, redirecting to login")
        return redirect('login')
    try:
        #student = Student.objects.get(user=request.user)
        logger.debug(f"Student found: {student_info}")
        return render(request, 'auth/student_dashboard.html', {'student': student_info})
    except Student.DoesNotExist:
        logger.error("No student associated with this user")
    user = request.user
    if user.is_authenticated:
        try:
            #student_info = Student.objects.get(user=user)
            return render(request, 'auth/student_dashboard.html')
        except Student.DoesNotExist:
            pass

        logger.error("Student object does not exist for the user")
        return HttpResponse("Student not found", status=404)

    if request.method == 'POST':
        semester_form = SemesterForm(request.POST)
        class_form = ClassForm(request.POST)
        if semester_form.is_valid() and class_form.is_valid():
            selected_semester = semester_form.cleaned_data['name']
            selected_class = class_form.cleaned_data['name']
            attendance_records = attendance_records.filter(
                class_attended__semester=selected_semester, 
                class_attended=selected_class
            )
    else:
        semester_form = SemesterForm()
        class_form = ClassForm()

    context = {
        'semesters': semesters,
        'classes': classes,
        'attendance_records': attendance_records,
        'semester_form': semester_form,
        'class_form': class_form,
    }
    return render(request, 'student_dashboard.html', context)

    # Any other logic and a final return statement
    logger.debug("Exiting student_dashboard view")
    return HttpResponse("Some default response or error page")

    
@auth
def teacher_dashboard(request):
    logger = logging.getLogger(__name__)
    logger.debug("Entering teacher_dashboard view")
    if not request.user.is_authenticated:
        logger.warning("User not authenticated, redirecting to login")
        return redirect('login')
    try:
        teacher = Teacher.objects.get(user=request.user)
        logger.debug(f"Teacher found: {teacher}")
        return render(request, 'auth/teacher_dashboard.html', {'teacher': teacher})
    except Teacher.DoesNotExist:
        logger.error("No teacher associated with this user")
    user = request.user
    if user.is_authenticated:
        try:
            teacher = Teacher.objects.get(user=user)
            return render(request, 'auth/teacher_dashboard.html')
        except Teacher.DoesNotExist:
            pass

        logger.error("Teacher object does not exist for the user")
        return HttpResponse("Teacher not found", status=404)

    # Any other logic and a final return statement
    logger.debug("Exiting teacher_dashboard view")
    return HttpResponse("Some default response or error page")

# LOGOUT 

def logout_view(request):
    logout(request)
    return redirect('login')



