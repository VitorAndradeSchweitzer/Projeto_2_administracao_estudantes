from django.contrib import admin
from .models import Teacher, Moderator, Student, Class

admin.site.register(Teacher)
admin.site.register(Moderator)
admin.site.register(Student)
admin.site.register(Class)
