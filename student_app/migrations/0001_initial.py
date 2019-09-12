# Generated by Django 2.2.5 on 2019-09-12 14:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=4)),
                ('hod', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('student_id', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=8)),
                ('register_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app.Class')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('staff_id', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=8)),
                ('designation', models.CharField(max_length=20)),
                ('register_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('_classes', models.ManyToManyField(to='student_app.Class')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app.Department')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app.Department'),
        ),
    ]
