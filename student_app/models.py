from django.db import models
from django.utils import timezone

# Create your models here.
class Student(models.Model):

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100)
    roll_no = models.BigIntegerField()
    gender = models.CharField(max_length=8)
    department = models.CharField(max_length=4)
    register_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}'.format(self.username)