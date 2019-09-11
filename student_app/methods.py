from .models import *


def student_context(id):
    student = Student.objects.filter(student_id=id).get()
    context = {
        'student' : student
    }
    return context


def staff_context(id):
    cc = False
    staff = Staff.objects.filter(staff_id=id).get()
    if Class.objects.filter(coordinator=staff).exists():
        _class = Class.objects.filter(coordinator=staff)[0]
        cc = True
    context = {
        'staff' : staff,
        'cc' : cc,
        'class' :  _class.name if cc == True else 'None'
    }
    return context