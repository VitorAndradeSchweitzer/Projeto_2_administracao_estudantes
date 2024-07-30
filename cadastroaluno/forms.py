from django import forms
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Student, Class, Teacher, Moderator
from django.utils import timezone


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    school = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        user= User.objects.filter(username=username).first()
        if user:
             raise forms.ValidationError('Username already in use')

        if not username.isalpha():
            raise forms.ValidationError('username should only contain letters and cannot be empty. ')
       
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password:
            raise forms.ValidationError('Password cannot be empty')
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')


        email_filter= User.objects.filter(email=email).first()
        if email_filter:
             raise forms.ValidationError('Email already in use')

        if '@' not in email or '.com' not in email:
            raise forms.ValidationError('Email invalid')
        if not email:
            raise forms.ValidationError('Email should not be empty')
        return email
    def clean_first_name(self):
         first_name = self.cleaned_data.get('first_name')
        
         if not first_name.isalpha():
            raise forms.ValidationError("should only contain letters and cannot be empty")
                
         return first_name
    def clean_last_name(self):
         last_name = self.cleaned_data.get('last_name')
        
         if not last_name.isalpha():
            raise forms.ValidationError("Last name should only contain letters and cannot be empty")
                
         return last_name
    def clean_school(self):
         school = self.cleaned_data.get('school')
        
         if not school.isalpha():
            raise forms.ValidationError("School should only contain letters and cannot be empty")
                
         return school
    

class NewStudentForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    responsable = forms.CharField(max_length=15)
    inscription_date = forms.DateField()
    matricula = forms.IntegerField()

    class Meta:
        model = Student
        fields = ['name', 'last_name', 'responsable', 'inscription_date', 'matricula']
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise ValidationError('Name should only contain letters and cannot be empty')
        return name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError('Last name should only contain letters and cannot be empty')
        return last_name

    def clean_responsable(self):
        responsable = self.cleaned_data.get('responsable')
        if not responsable.isdigit():
            raise ValidationError('Responsable should only contain letters and cannot be empty')
        return responsable

    def clean_inscription_date(self):
        inscription_date = self.cleaned_data.get('inscription_date')
        if inscription_date > timezone.now().date():
            raise ValidationError('Inscription date cannot be in the future.')
        return inscription_date

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        if not isinstance(matricula, int):
            raise ValidationError('Matricula should be a number.')
        if matricula < 0:
            raise ValidationError('Matricula cannot be negative.')
        return matricula
    



class NewTeacherForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    subject = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254) 
    password = forms.CharField(max_length=30, widget=forms.PasswordInput) 

    class Meta:
        model = Teacher
        fields = ['name', 'last_name', 'subject', 'email', 'password']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise ValidationError('O nome deve conter apenas letras.')
        return name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError('O sobrenome deve conter apenas letras.')
        return last_name

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if not subject:
            raise ValidationError('Subject cannot be null')
        return subject

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email should not be empty')
        
        try:
            forms.EmailField().clean(email)
        except ValidationError:
            raise ValidationError('Invalid email format')

        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError('Password cannot be empty')
        return password
    
class NewClassForm(forms.ModelForm):
    name = forms.CharField(max_length=30)    
    teachers = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.all(),
        widget=forms.SelectMultiple,
        required=True
    )

  
    class Meta:
        model = Class
        fields = ['teachers', 'name']
 
    def clean_teachers(self):
        teachers = self.cleaned_data.get('teachers')
        if not teachers:
            raise forms.ValidationError('Pelo menos um professor deve ser selecionado.')
        return teachers
    def clean_name(self):
        name= self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Name field cant be empty')
        return name