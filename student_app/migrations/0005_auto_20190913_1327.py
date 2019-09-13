# Generated by Django 2.2.5 on 2019-09-13 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0004_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='_class',
        ),
        migrations.AddField(
            model_name='class',
            name='subjects',
            field=models.ManyToManyField(to='student_app.Subject'),
        ),
    ]
