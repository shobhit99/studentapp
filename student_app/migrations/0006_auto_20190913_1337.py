# Generated by Django 2.2.5 on 2019-09-13 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0005_auto_20190913_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student_app.Subject'),
        ),
    ]