from rest_framework import viewsets
from cadastroaluno.api import serializers
from cadastroaluno import models
from django.contrib.auth.models import User
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()

class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeacherSerializer
    queryset = models.Teacher.objects.all()

class ClassViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClassSerializer
    queryset = models.Class.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

class ModeratorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ModeratorSerializer
    queryset = models.Moderator.objects.all()
