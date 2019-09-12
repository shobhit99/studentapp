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
    classes = staff.classes.all()
    if len(classes):
        cc = True
    context = {
        'staff' : staff,
        'cc' : cc, 
        'classes' : classes
    }
    return context