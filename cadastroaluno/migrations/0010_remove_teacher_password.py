# Generated by Django 5.0.7 on 2024-07-26 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastroaluno', '0009_student_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='password',
        ),
    ]
