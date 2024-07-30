from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, NewStudentForm, NewTeacherForm, NewClassForm
import requests
import json
from django.contrib.auth import login, authenticate
from .models import Teacher, Moderator, Student, Class



def Loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_data = {
            'username': username,
            'password': password,
        }

        url = 'http://127.0.0.1:8000/api/token/'

        try:
            
            response = requests.post(url, data=login_data)
            if response.status_code == 200:
                tokens = response.json()
                access_token = tokens['access']
                refresh_token = tokens['refresh']


                response = redirect('home/')
                response.set_cookie('jwt_token', access_token, httponly=True, secure=True)
              
                
                username = request.POST.get('username')
                user = User.objects.filter(username=username).first()
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return response
                else:
                    return HttpResponse('usuario não autentificado')
            else:
                response_content = response.content.decode('utf-8')
                return HttpResponse(f'Algo deu errado: {response_content}')
        except requests.exceptions.RequestException as e:
            return HttpResponse(f'Erro na requisição: {str(e)}')
    else:
        return render(request, 'pages/loginpage.html', context={
            'loginpage': True})




def create_accont(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            username = request.POST.get('username')
            user = User.objects.filter(username=username).first()

            school = request.POST.get('school')
            moderator = Moderator.objects.create(user=user,school= school)
            moderator.save()
            login(request, user)

            return redirect('home/') 
        else:
            return render(request, 'pages/loginpage.html', context={
                'form': form})
    else:
               return render(request, 'pages/loginpage.html')




def home(request):
    moderator = Moderator.objects.filter(user=request.user).first()
    students = Student.objects.filter(moderator=moderator).order_by('turma')
    classes = Class.objects.filter(moderator=moderator).order_by('name')
    
    students_by_class = {}
    for student in students:
        turma_name = student.turma.name 
        if turma_name not in students_by_class:
            students_by_class[turma_name] = []
        students_by_class[turma_name].append(student)
    
    return render(request, 'pages/home.html', context={
       
        'user':request.user,
        'students': students,
        'classes': classes,
        'students_by_class': students_by_class,
        
    })



def new_class(request):

    if request.method == 'GET':
        moderator = Moderator.objects.filter(user=request.user).first()
        teachers = Teacher.objects.filter(moderator=moderator.id)
        return render(request, 'pages/new_class.html', context={
        'teachers': teachers
        })
    


    form = NewClassForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        moderator = Moderator.objects.filter(user = request.user).first()
        data['moderator'] = moderator.id
        data['teachers'] = [teacher.id for teacher in data['teachers']]
        url = 'http://127.0.0.1:8000/api/class/'
        print(data)
        
        token = request.COOKIES.get('jwt_token')
        headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        response = requests.post(url, json=data, headers=headers)
          
        if response.status_code == 201:
            return HttpResponse('classe craida')
        return HttpResponse(f'{data}')
    return HttpResponse(f'formulario nao foi {form.errors}')




def new_student(request):
    moderator = Moderator.objects.filter(user = request.user).first()
    
    if request.method == 'GET':
        classes = Class.objects.filter(moderator=moderator)
        return render(request, 'pages/new_student.html', context={
            'classes': classes,
            "moderator": moderator
        })
    


    form = NewStudentForm(request.POST) 
    if form.is_valid():
        url = 'http://127.0.0.1:8000/api/students/'
    
        moderator = Moderator.objects.filter(user = request.user).first()
        data = form.cleaned_data
        
        data['moderator'] = moderator.id
        data['turma'] = request.POST.get('class')
        data['password'] = f"{moderator.id} ,{data['matricula']}"
        data['inscription_date'] = data['inscription_date'].strftime('%Y-%m-%d')
        token = request.COOKIES.get('jwt_token')
        headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
    
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            return HttpResponse(f'{data}')
        else:
            return HttpResponse(f'{response.text}')
    return HttpResponse(f'nao foi, {form.errors}')




def new_teacher(request):
    moderator = Moderator.objects.filter(user=request.user).first()
    if request.method == 'GET':
        return render(request, 'pages/new_teacher.html', context={
         'moderator': moderator
        })
    else:
      form = NewTeacherForm(request.POST)
      if form.is_valid():
          data = form.cleaned_data
          moderator = Moderator.objects.filter(user=request.user).first()
          data['moderator'] = moderator.id
          url =  'http://127.0.0.1:8000/api/teacher/'
          token = request.COOKIES.get('jwt_token')
          headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
          response = requests.post(url, json=data, headers=headers)
          if response.status_code == 201:
              return home(request)
          else:
                return HttpResponse(f'Response: {response.status_code}, {response.text}')
      else:
            return HttpResponse(f'Form is not valid: {form.errors}')