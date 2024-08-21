from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, NewStudentForm, NewTeacherForm, NewClassForm
from .models import Teacher, Moderator, Student, Class
from rolepermissions.roles import assign_role
import requests


def get_auth_headers(request):
  
    token = request.COOKIES.get('jwt_token')
    if not token:
        return None
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


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

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    response = redirect('home/')
                    response.set_cookie('jwt_token', access_token, httponly=True, secure=True)
                    return response
                else:
                    return HttpResponse('Usuário não autenticado')
            else:
                response_content = response.content.decode('utf-8')
                return HttpResponse(f'Algo deu errado: {response_content}')
        except requests.exceptions.RequestException as e:
            return HttpResponse(f'Erro na requisição: {str(e)}')
    else:
        return render(request, 'pages/loginpage.html', context={'loginpage': True})


def create_accont(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            user = User.objects.filter(username=username).first()
            assign_role(user, 'moderator')
            school = request.POST.get('school')
            moderator = Moderator.objects.create(user=user, school=school)
            login(request, user)
            return redirect('home/')
        else:
            return render(request, 'pages/loginpage.html', context={'form': form})
    else:
        return render(request, 'pages/loginpage.html')


def home(request):
    user = request.user
    if user.groups.filter(name='moderator').exists():
        return home_moderator(request)
    if user.groups.filter(name='teacher').exists():
        return home_teacher(request)
    if user.groups.filter(name='student').exists():
        return home_student(request)


def home_moderator(request):
    moderator = Moderator.objects.filter(user=request.user).first()
    students = Student.objects.filter(moderator=moderator).order_by('turma')
    classes = Class.objects.filter(moderator=moderator).order_by('name')

    students_by_class = {}
    for student in students:
        turma_name = student.turma.name
        if turma_name not in students_by_class:
            students_by_class[turma_name] = []
        students_by_class[turma_name].append(student)

    return render(request, 'pages/home/home.html', context={
        'user': request.user,
        'moderator': moderator,
        'students': students,
        'classes': classes,
        'students_by_class': students_by_class,
    })


def home_teacher(request):
    return render(request, 'pages/home/home_teacher.html')


def home_student(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'pages/home/home_student.html', context={
        'student': student 
    })











def new_class(request):
    if request.method == 'GET':
        moderator = Moderator.objects.filter(user=request.user).first()
        teachers = Teacher.objects.filter(moderator=moderator.id)
        return render(request, 'pages/new_class.html', context={'teachers': teachers})

    form = NewClassForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        moderator = Moderator.objects.filter(user=request.user).first()
        data['moderator'] = moderator.id
        data['teachers'] = [teacher.id for teacher in data['teachers']]
        url = 'http://127.0.0.1:8000/api/class/'

        headers = get_auth_headers(request)
        if headers is None:
            return HttpResponse('Token não encontrado')

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            return home(request)

    return render(request, 'pages/new_class.html', context={'form': form})


def new_student(request):
    moderator = Moderator.objects.filter(user=request.user).first()

    if request.method == 'GET':
        classes = Class.objects.filter(moderator=moderator)
        return render(request, 'pages/new_student.html', context={
            'classes': classes,
            "moderator": moderator
        })

    form = NewStudentForm(request.POST)
    if form.is_valid():
        url = 'http://127.0.0.1:8000/api/students/'

        data = form.cleaned_data
        data['moderator'] = moderator.id
        data['turma'] = request.POST.get('class')
        data['password'] = f"{data['matricula']}"
        data['inscription_date'] = data['inscription_date'].strftime('%Y-%m-%d')

        headers = get_auth_headers(request)
        if headers is None:
            return HttpResponse('Token não encontrado')

        new_student = User(username=f"{data['moderator']}{data['name']}{data['last_name']}",
                           first_name=data['name'], last_name=data['last_name'])
        new_student.set_password(data['password'])
        new_student.save()
        assign_role(new_student, 'student')
        data['user'] = new_student.id
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            return home(request)

        return HttpResponse(f'{response.text}')
    return render(request, 'pages/new_student.html', context={'form': form})


def new_teacher(request):
    moderator = Moderator.objects.filter(user=request.user).first()
    if request.method == 'GET':
        return render(request, 'pages/new_teacher.html', context={'moderator': moderator})

    form = NewTeacherForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        moderator = Moderator.objects.filter(user=request.user).first()
        data['moderator'] = moderator.id
        url = 'http://127.0.0.1:8000/api/teacher/'

        headers = get_auth_headers(request)
        if headers is None:
            return HttpResponse('Token não encontrado')

        new_teacher = User(username=f"{data['moderator']}{data['name']}{data['last_name']}",
                           first_name=data['name'], last_name=data['last_name'], email=data['email'])
        new_teacher.set_password(data['password'])
        new_teacher.save()
        assign_role(new_teacher, 'teacher')
        data['user'] = new_teacher.id
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            return home(request)
        else:
            return HttpResponse(f'Response: {response.status_code}, {response.text}')
    else:
        return render(request, 'pages/new_teacher.html', context={'form': form})


def student_profile(request, student_id):
    url = f'http://127.0.0.1:8000/api/students/{student_id}'

    headers = get_auth_headers(request)
    if headers is None:
        return HttpResponse('Token não encontrado')

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        student_data = response.json()
        classe = Class.objects.get(id=student_data['turma'])
        return render(request, 'pages/student_profile.html', context={
            'student': student_data,
            'class': classe
        })
    else:
        return HttpResponse('Algo deu errado')
    
def student_teachers(request):
    student = get_object_or_404(Student, user=request.user)

    return render(request, 'pages/student_pages/teachers_page.html', context={
    "student": student})


from django.core.mail import EmailMessage

def enviar_email_com_anexo():
    email = EmailMessage(
        'Assunto do Email',
        'Aqui está a mensagem do email.',

        ['vitor2.a.schweitzer@gmail.com']
    )

    email.send()

enviar_email_com_anexo()
