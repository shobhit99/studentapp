# Generated by Django 2.2.5 on 2019-09-14 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0013_remove_book_copies'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_pic',
            field=models.CharField(default='default', max_length=100),
        ),
    ]