from django import forms
#from .models import Semester, Class, User
from .models import Class, User

class SemesterForm(forms.ModelForm):
    class Meta:
      #  model = Semester
        fields = ['name']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        #fields = ['name', 'semester']
        fields = ['name']

class StudentRegistrationForm(forms.ModelForm):
    # Define form fields here
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

