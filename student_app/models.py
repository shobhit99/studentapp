from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

# Create your models here.
class Department(models.Model):

    name = models.CharField(max_length=4)
    hod  = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    
    name    = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Class(models.Model):

    name          = models.CharField(max_length=25)
    department    = models.ForeignKey(Department, on_delete = models.CASCADE)
    subjects      = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name


class Staff(models.Model):
    
    first_name      = models.CharField(max_length=25)
    last_name       = models.CharField(max_length=25)
    email           = models.EmailField(max_length=50)
    password        = models.CharField(max_length=100)
    staff_id        = models.CharField(max_length=15)
    gender          = models.CharField(max_length=8)
    department      = models.ForeignKey(Department, on_delete = models.CASCADE)
    designation     = models.CharField(max_length=20)
    register_time   = models.DateTimeField(default=timezone.now)
    classes         = models.ManyToManyField(Class)

    def __str__(self):
        return '{}'.format(self.first_name + self.last_name)


class Student(models.Model):
    
    first_name      = models.CharField(max_length=25)
    last_name       = models.CharField(max_length=25)
    email           = models.EmailField(max_length=50)
    password        = models.CharField(max_length=100)
    student_id      = models.CharField(max_length=15)
    gender          = models.CharField(max_length=8)
    department      = models.ForeignKey(Department, on_delete = models.CASCADE)
    _class          = models.ForeignKey(Class, on_delete = models.CASCADE)
    register_time   = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Attendance(models.Model):

    marked_by       = models.ForeignKey(Staff, on_delete = models.DO_NOTHING)
    unique_id       = models.CharField(max_length=100)
    student         = models.ForeignKey(Student, on_delete = models.DO_NOTHING)
    status          = models.BooleanField()
    subject         = models.ForeignKey(Subject, on_delete = models.DO_NOTHING)
    taken_time      = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} {} {}'.format(self.student, self.status, self.taken_time)


class Notice(models.Model):

    title       = models.CharField(max_length=100)
    notice      = models.TextField()
    added_by    = models.ForeignKey(Staff, on_delete = models.CASCADE)
    class_obj   = models.ManyToManyField(Class)

    def __str__(self):
        return self.title


class Exam(models.Model):
    
    name         = models.CharField(max_length=5)
    subject      = models.ForeignKey(Subject, on_delete = models.DO_NOTHING)
    marks        = models.IntegerField()
    student      = models.ForeignKey(Student, on_delete = models.DO_NOTHING)
    publish_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return "{} {} {} {}".format(self.name, self.subject, self.marks, self.student)


class Book(models.Model):

    name         = models.CharField(max_length=100)
    isbn         = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BorrowRecord(models.Model):

    student     = models.ForeignKey(Student, on_delete = models.CASCADE )
    book        = models.ForeignKey(Book, on_delete = models.DO_NOTHING )
    borrow_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} {} {}".format(self.student, self.book, self.borrow_time)