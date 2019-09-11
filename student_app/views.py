from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import *

# Create your views here.
def index(request):
    if request.method == 'POST':
        if 'login-form' in request.POST:

            login_form = StudentLogin(request.POST)
            
            if login_form.is_valid():
                
                if Student.objects.filter(student_id=request.POST['user_login']).exists():
                    student = Student.objects.filter(student_id=request.POST['user_login'])[0]
                    if check_password(request.POST['user_password'], student.password):
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
                    return redirect('/')

                hashed_password = make_password(request.POST['password'], salt=None, hasher='default')
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
                
                if Staff.objects.filter(staff_id=request.POST['staff_login']).exists():
                    staff = Staff.objects.filter(staff_id=request.POST['staff_login'])[0]
                    if check_password(request.POST['staff_password'], staff.password):
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
                    return redirect('staff')

                hashed_password = make_password(request.POST['password'], salt=None, hasher='default')
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
    
    if request.session['user_type'] == 'student':
        student = Student.objects.filter(student_id=request.session['student_id']).get()
        context = {
            'name' : "{} {}".format(student.first_name, student.last_name)
        }
        return render(request, 'student_app/dashboard.html', context)

    elif request.session['user_type'] == 'staff':
        staff = Staff.objects.filter(staff_id=request.session['staff_id']).get()
        context = {
            'name' : "{} {}".format(staff.first_name, staff.last_name)
        }
        return render(request, 'staff/dashboard.html', context)
    else:
        return redirect('/')


def logout(request):

    del request.session['student_id']

    return redirect('/')