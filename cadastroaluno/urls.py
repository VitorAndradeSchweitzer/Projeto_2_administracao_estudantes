
from django.urls import path
from . import views
app_name = 'Admin'
urlpatterns = [
    path('', views.Loginpage, name='loginpage'),
    path('create_accont', views.create_accont,name='create_accont'),
    path('home/', views.home, name='home'),
    path('moderator/', views.home_moderator, name='home_moderator'),
    path('new_student/', views.new_student, name='new_student'),
    path('new_class/', views.new_class, name='new_class'),
    path('new_teacher/', views.new_teacher, name='new_teacher'),
    path('student_profile/<int:student_id>', views.student_profile, name='student_profile'),
]
