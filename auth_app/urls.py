from django.urls import path
from . import views
from .views import register_student
from.views import register_teacher
from  .views import student_dashboard
from .views import teacher_dashboard


urlpatterns = [
# path('',views.register_view,name='register'),
    path('',views.index_view,name='index'),
    path('login/',views.login_view,name='login'),
    path('student_register/', views.register_student, name='student_register'),  # URL for student registration
    path('teacher_register/', views.register_teacher, name='teacher_register'),
    path('logout/',views.logout_view,name='logout'),
    path('student_dashboard/',views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/',views.teacher_dashboard, name='teacher_dashboard'),
    #path('dummy_view/', views.dummy_view)
    #path('_debug_/', include('debug_toolbar.urls')),
    #path('display-student-dashboard/',views.student_view ,name='student-dashboard')
]