from rest_framework import serializers
from cadastroaluno import models


from django.contrib.auth.models import User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = '__all__'
 

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Teacher

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Class

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model =  User
        fields = ('id','username', 'email', 'password', 'first_name', 'last_name')  
        extra_kwargs = {'password': {'write_only': True}} 
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

class ModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Moderator
        


class Moderator_AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Moderator_Advice