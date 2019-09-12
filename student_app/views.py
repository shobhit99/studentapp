from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import *
from .methods import *
import uuid

# Create your views here.
def index(request):

    if request.method == 'POST':
        if 'login-form' in request.POST:

            login_form = StudentLogin(request.POST)
            
            if login_form.is_valid():
                
                # If given user id exists then check for password
                if Student.objects.filter(student_id=request.POST['user_login']).exists():
                    student = Student.objects.filter(student_id=request.POST['user_login'])[0]
                    if check_password(request.POST['user_password'], student.password):
                        # user_type in sessions variable will decide dashboard and contents
                        request.session['user_type'] = 'student'
                        request.session['student_id'] = student.student_id
                        return redirect('dashboard')
                    else:
                        messages.error(request, 'Login ID or password incorrect')
                        return redirect('/')
                
        elif 'register-form' in request.POST:
            
            register_form = StudentRegister(request.POST)
            
            if register_form.is_valid():

                errors = False
                if request.POST['password'] != request.POST['repeat_password']:
                    messages.add_message(request, messages.ERROR, 'Passwords donot match!')
                    errors = True

                if Student.objects.filter(email=request.POST['email']).exists() or Student.objects.filter(student_id=request.POST['student_id']).exists():
                    messages.add_message(request, messages.ERROR, 'Email or Student ID already registered')
                    errors = True

                if errors:
                    # If passwords donot match of email / user id already registered then display error messages
                    return redirect('/')

                hashed_password = make_password(request.POST['password'], salt=None, hasher='default')
                # Department and Class are foreign key in Student table
                department  = Department.objects.filter(name=request.POST['departments']).get()
                _class      = Class.objects.filter(name=request.POST['year']+request.POST['section']).get() 
                new_student = Student(
                    first_name  = request.POST['first_name'],
                    last_name   = request.POST['last_name'],
                    email       = request.POST['email'],
                    password    = hashed_password,
                    student_id  = request.POST['student_id'],
                    gender      = request.POST['gender'],
                    _class      = _class,
                    department  = department,
                )
                new_student.save()
                messages.success(request, 'Registered Successfully')
                return redirect('/')
      
    register_form  = StudentRegister()
    login_form     = StudentLogin()
    context = {'register_form' : register_form, 'login_form' : login_form }
    return render(request, 'student_app/index.html', context)


def staff(request):

    if request.method == 'POST':
        if 'login-form' in request.POST:

            login_form = StaffLogin(request.POST)
            
            if login_form.is_valid():
                # If staff id valid check password
                if Staff.objects.filter(staff_id=request.POST['staff_login']).exists():
                    staff = Staff.objects.filter(staff_id=request.POST['staff_login'])[0]
                    if check_password(request.POST['staff_password'], staff.password):
                        # user type will decide contents
                        request.session['user_type'] = 'staff'
                        request.session['staff_id']  = staff.staff_id
                        return redirect('dashboard')
                    else:
                        messages.error(request, 'Login ID or password incorrect')
                        return redirect('staff')
                

        elif 'register-form' in request.POST:
            
            register_form = StaffRegister(request.POST)
            
            if register_form.is_valid():

                errors = False
                if request.POST['password'] != request.POST['repeat_password']:
                    messages.add_message(request, messages.ERROR, 'Passwords donot match!')
                    errors = True

                if Staff.objects.filter(email=request.POST['email']).exists() or Staff.objects.filter(staff_id=request.POST['staff_id']).exists():
                    messages.add_message(request, messages.ERROR, 'Email or Staff ID already registered')
                    errors = True

                if errors:
                    # display errors if passwords donot match or email / user id already registered
                    return redirect('staff')

                hashed_password = make_password(request.POST['password'], salt=None, hasher='default')
                # Department is foreign key in Staff table
                department  = Department.objects.filter(name=request.POST['departments']).get()
                new_staff = Staff(
                    first_name  = request.POST['first_name'],
                    last_name   = request.POST['last_name'],
                    email       = request.POST['email'],
                    password    = hashed_password,
                    staff_id    = request.POST['staff_id'],
                    gender      = request.POST['gender'],
                    designation = request.POST['designation'],
                    department  = department,
                )
                new_staff.save()
                messages.success(request, 'Registered Successfully')
                return redirect('staff')

    register_form  = StaffRegister()
    login_form     = StaffLogin() 
    context = {'register_form' : register_form, 'login_form' : login_form }
    return render(request, 'staff/index.html', context)


def dashboard(request):

    # if not logged in then redirect to home page
    if 'user_type' not in request.session.keys():
        return redirect('/')
    
    # if user is student then display student dashboard
    if request.session['user_type'] == 'student':
        context = student_context(request.session['student_id'])
        return render(request, 'student_app/dashboard.html', context)

    # if user is staff then display staff's dashboard
    elif request.session['user_type'] == 'staff':
        context = staff_context(request.session['staff_id'])
        # If staff is a teacher in any class then cc is true then
        # "Attendance" section will be visible with list of classes 
        request.session['cc'] = context['cc']
        return render(request, 'staff/dashboard.html', context)


def profile(request):

    
    if 'user_type' not in request.session.keys():
        return redirect('/')

    if request.session['user_type'] == 'student':
        context = student_context(request.session['student_id'])
        return render(request, 'student_app/profile.html', context)

    elif request.session['user_type'] == 'staff':
        context = staff_context(request.session['staff_id'])
        request.session['cc'] = context['cc']
        return render(request, 'staff/profile.html', context)
    

def notice(request):
    
    if 'user_type' not in request.session.keys():
        return redirect('/')
    if request.session['cc'] == True:
        staff = Staff.objects.filter(staff_id=request.session['staff_id']).get()
        _class = Class.objects.filter(coordinator=staff)[0]
        students = _class.student_set.all()
        context = {
            'staff' : staff,
            'classes' : classes,
            'cc' : True
        }
        return render(request, 'staff/notice.html', context)
    else:
        return redirect('/')


def attendance(request, class_name):

    if 'user_type' not in request.session.keys():
        return redirect('/')

    if request.session['cc'] == True:
        if request.method == "POST":
            values      = request.POST.getlist('student_list[]')
            subject     = request.POST['subject']
            unique_id   = str(uuid.uuid4())
            staff = Staff.objects.filter(staff_id=request.session['staff_id']).get()
            _class = Class.objects.filter(name=class_name).get()
            students = _class.student_set.all()
            for student in students:
                new_record = Attendance(marked_by=staff, unique_id=unique_id, student = student, status = True if student.student_id in values else False, subject = subject)
                new_record.save()
            messages.success(request, 'Attendance added Successfully')
            return redirect('attendance', class_name=class_name)

        # _class object will be used to display student list from that class
        # _class gets list of all students from that class
        # classes if a list of classes to display in Attendance section if cc
        _class = Class.objects.filter(name=class_name).get()
        students = _class.student_set.all() 
        staff = Staff.objects.filter(staff_id=request.session['staff_id']).get()
        classes = staff.classes.all()
        context = {
            'staff' : staff,
            'classes' : classes,
            'students' : students,
            'class' : _class,
            'cc' : True
        }
        return render(request, 'staff/students.html', context)
    else:
        return redirect('/')


def student_attendance(request):

    if 'user_type' not in request.session.keys():
        return redirect('/')
    
    if request.session['user_type'] == 'student':
        context            = student_context(request.session['student_id'])
        student            = context['student']
        total_lectures     = Attendance.objects.filter(student=student).count()
        attended_lectures  = Attendance.objects.filter(student=student).filter(status=True).count()
        percent            = (attended_lectures / total_lectures) * 100
        context['attendance'] = percent
    return render(request, 'student_app/attendance.html', context)
    


def logout(request):

    for key in list(request.session.keys()):
        del request.session[key]

    return redirect('/')