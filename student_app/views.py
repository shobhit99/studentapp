from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    if request.method == 'POST':
        if 'login-form' in request.POST:
            messages.success(request, ('Thank you'))
            return redirect('index')

        elif 'register-form' in request.POST:

            register_form = StudentRegister(request.POST)
            if register_form.is_valid():
                new_student = Student(
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email'],
                    password = request.POST['password'],
                    roll_no = request.POST['roll_no'],
                    gender = request.POST['gender'],
                    department = request.POST['departments'],
                )
                new_student.save()
                return redirect('index')
      
    register_form = StudentRegister()
    login_form = StudentLogin()
    context = {'register_form' : register_form, 'login_form' : login_form }
    return render(request, 'student_app/index.html', context)