# Generated by Django 2.2.5 on 2019-09-13 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0006_auto_20190913_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('notice', models.TextField()),
                ('_class', models.ManyToManyField(to='student_app.Class')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app.Staff')),
            ],
        ),
    ]
