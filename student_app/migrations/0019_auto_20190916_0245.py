# Generated by Django 2.2.5 on 2019-09-15 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0018_auto_20190916_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mobile_no',
            field=models.IntegerField(null=True),
        ),
    ]