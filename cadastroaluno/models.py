from django.db import models
from django.contrib.auth.models import User


class Moderator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username
    

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    moderator = models.ForeignKey( Moderator, on_delete=models.CASCADE, null=1)
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='posts/covers/%y/%m/%d', null=True, blank=True)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    

class Class(models.Model):
    moderator = models.ForeignKey( Moderator, on_delete=models.CASCADE, null=1)
    teachers = models.ManyToManyField(Teacher, related_name='classes')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

    
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    moderator = models.ForeignKey( Moderator, on_delete=models.CASCADE, null=1)
    turma = models.ForeignKey('Class',  on_delete=models.CASCADE, default=False)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    responsable = models.CharField(max_length=50)
    inscription_date = models.DateField()
    matricula = models.IntegerField()
    photo = models.ImageField(upload_to='posts/covers/%y/%m/%d', null=True, blank=True)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.name