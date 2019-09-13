from .models import *


def student_context(id):
    student     = Student.objects.filter(student_id=id).get()
    notice_count = student._class.notice_set.all().count()
    context = {
        'student'      : student,
        'notice_count' : notice_count
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