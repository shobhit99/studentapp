from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

# Create your models here.
class Student(models.Model):

    first_name      = models.CharField(max_length=25)
    last_name       = models.CharField(max_length=25)
    email           = models.EmailField(max_length=50)
    password        = models.CharField(max_length=100)
    student_id      = models.CharField(max_length=15)
    gender          = models.CharField(max_length=8)
    department      = models.CharField(max_length=4)
    _class          = models.CharField(max_length=5)
    register_time   = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}'.format(self.first_name + self.last_name)