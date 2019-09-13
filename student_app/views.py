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

                        for key in list(request.session.keys()):        # Delete previous session if any
                            del request.session[key]

                        request.session['user_type'] = 'student'        # user_type in sessions variable will decide dashboard and contents
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
                if Staff.objects.filter(staff_id=request.POST['staff_login']).exists():     # If staff id valid check password
                    staff = Staff.objects.filter(staff_id=request.POST['staff_login'])[0]
                    if check_password(request.POST['staff_password'], staff.password):

                        for key in list(request.session.keys()):        # Delete previous session if any
                            del request.session[key]
                        
                        request.session['user_type'] = 'staff'          # user type will decide contents
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

    if 'user_type' not in request.session.keys():                       # if not logged in then redirect to home page
        return redirect('/')
    
    
    if request.session['user_type'] == 'student':                       # if user is student then display student dashboard
        context = student_context(request.session['student_id'])
        return render(request, 'student_app/dashboard.html', context)

    elif request.session['user_type'] == 'staff':                       # if user is staff then display staff's dashboard
        context = staff_context(request.session['staff_id'])
        request.session['cc'] = context['cc']                           # if staff then "Attendance" menu will be visible
        return render(request, 'staff/dashboard.html', context)

def books(request, action='view'):

    if 'user_type' not in request.session.keys():                       
        return redirect('/')
    
    
    if request.session['user_type'] == 'student':
        context = student_context(request.session['student_id'])
        return render(request, 'student_app/dashboard.html', context)

    elif request.session['user_type'] == 'staff':
        context = staff_context(request.session['staff_id'])

        if action == 'add_record':
            if "search" in request.POST:                # Return matching books
                book_name = request.POST['book_name']
                results   = Book.objects.filter(name__contains=book_name) if Book.objects.filter(name__contains=book_name).count() else False
                if not results:
                    messages.success(request, "No Records found")
                else:
                    context['search'] = True
                    context['books']  = results
                    return render(request, 'staff/add-record.html', context)
                return redirect('books', action='add_record')

            elif "lend" in request.POST:               # Add borrow record
                student_id = request.POST['student_id']
                isbn       = request.POST['isbn']

                if Student.objects.filter(student_id=student_id).exists() and Book.objects.filter(isbn=isbn).exists():
                    student = Student.objects.filter(student_id=student_id).get()
                    book    = Book.objects.filter(isbn=isbn).get()
                else:
                    messages.error(request, "Invalid ISBN or Student ID")
                    return redirect('books', action='add_record')


                new_borrow_record = BorrowRecord(student=student, book=book)
                new_borrow_record.save()
                messages.success(request, "Success !")
                return redirect('books', action='add_record')


            return render(request, 'staff/add-record.html', context)

        elif action == "add":
            if request.method == "POST":
                book_name = request.POST['book_name']
                isbn      = request.POST['isbn']
                new_book  = Book(name=book_name, isbn=isbn)
                new_book.save()
                messages.success(request, "Book added to Database!")
                return redirect('books', action='add')
            return render(request, 'staff/add-book.html', context)

        elif action == "view":
            books   = Book.objects.all()
            context['books'] = books
            return render(request, 'staff/view-books.html', context)

        

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
    

def notice(request, action='view'):
    
    if 'user_type' not in request.session.keys():
        return redirect('/')
    
    if request.session['user_type'] == 'student':
        context             = student_context(request.session['student_id'])
        no_notice           = True if context['student']._class.notice_set.all().count() == 0 else False
        if no_notice:
            context['notices'] = no_notice
        else:
            context['notices']  = context['student']._class.notice_set.all()[:10]
        return render(request, 'student_app/notice.html', context)

    elif request.session['user_type'] == 'staff':
        context = staff_context(request.session['staff_id'])
        request.session['cc'] = context['cc']
        if request.session['cc'] == True:
            staff       = Staff.objects.filter(staff_id=request.session['staff_id']).get()
            classes     = staff.classes.all()
            notices     = staff.notice_set.all()[:10]
            context = {
                'staff'   : staff,
                'classes' : classes,
                'notices' : notices,
                'cc' : True
            }
            
            if action == 'view':
                if request.method == "POST":
                    noteid  = request.POST['id']
                    Notice.objects.filter(pk=noteid).delete()
                    messages.success(request, "Notice Deleted!")
                    return redirect('notice', action='view')
                return render(request, 'staff/view-notice.html', context)
                
            else:
                if request.method == "POST":

                    title      = request.POST['title']
                    notice     = request.POST['notice']
                    class_list = request.POST.getlist('class_list[]')

                    notice = Notice(title=title, notice=notice, added_by=staff)
                    notice.save()
                    for class_name in class_list:
                        c = Class.objects.filter(name=class_name).get()
                        notice.class_obj.add(c)
                    messages.success(request, "Notice Added!")
                    return redirect('notice', action='add')
                
                return render(request, 'staff/add-notice.html', context)
        else:
            return redirect('/')


def attendance(request, class_name):

    if 'user_type' not in request.session.keys():
        return redirect('/')

    if request.session['cc'] == True:
        if request.method == "POST":
            values      = request.POST.getlist('student_list[]')
            subject     = Subject.objects.filter(name=request.POST['subject']).get()
            unique_id   = str(uuid.uuid4())
            staff       = Staff.objects.filter(staff_id=request.session['staff_id']).get()
            _class      = Class.objects.filter(name=class_name).get()
            students    = _class.student_set.all()
            for student in students:
                new_record = Attendance(marked_by=staff, unique_id=unique_id, student = student, status = True if student.student_id in values else False, subject = subject)
                new_record.save()
            messages.success(request, 'Attendance added Successfully')
            return redirect('attendance', class_name=class_name)

        _class      = Class.objects.filter(name=class_name).get()  # _class object will be used to display student list from that class
        students    = _class.student_set.all()                     # _class gets list of all students from that class
        staff       = Staff.objects.filter(staff_id=request.session['staff_id']).get()
        subjects    = _class.subjects.all()
        classes     = staff.classes.all()                          # classes if a list of classes to display in Attendance section if cc
        context     = {
            'staff'     : staff,
            'classes'   : classes,
            'students'  : students,
            'class'     : _class,
            'subjects'  : subjects,
            'cc'        : True
        }
        return render(request, 'staff/students.html', context)
    else:
        return redirect('/')


def student_attendance(request):

    if 'user_type' not in request.session.keys():
        return redirect('/')
    
    if request.session['user_type'] == 'student':
        context            = student_context(request.session['student_id'])
        student            = context['student']     # student object
        _class             = student._class         # get class of student
        subjects           = _class.subjects.all()  # get subjects of student
        attendance = {}
        percent_count = 0
        for subject in subjects:
            total           = Attendance.objects.filter(student=student).filter(subject=subject).count()                        # total lectures conducted
            attended        = Attendance.objects.filter(student=student).filter(subject=subject).filter(status=True).count()    # total lectures attended by student
            percent         = 0.0 if not total else (attended/total)*100 # Avoid division if total is zero
            percent_count += percent
            attendance[subject.name] = [
                total, 
                attended,
                "{:.2f}".format(percent)
            ]
        avg_attendance = percent_count / len(subjects)                  # Calculate Average attendance
        context['attendance'] = attendance
        context['avg_attendance'] = "{:.2f}".format(avg_attendance)
    return render(request, 'student_app/attendance.html', context)
    

def results(request):

    if request.session['user_type'] == 'student':
        context   = student_context(request.session['student_id'])
        if context['student'].exam_set.filter(name='unit1').count():
            unit1 = context['student'].exam_set.filter(name='unit1').get()
        else:
            unit1 = False
        if context['student'].exam_set.filter(name='unit2').count():
            unit2 = context['student'].exam_set.filter(name='unit1').get()
        else:
            unit2 = False
        context['unit1'] = unit1
        context['unit2'] = unit2
        return render(request, 'student_app/results.html', context)
    else:
        return redirect('/')

def exam(request, class_name):

    if 'user_type' not in request.session.keys():
        return redirect('/')
        
    if request.session['cc'] == True:
        if request.method == "POST":
            student_ids = request.POST.getlist('student_list[]')
            mark_list   = request.POST.getlist('mark_list[]')
            subject     = Subject.objects.filter(name=request.POST['subject']).get()
            exam        = request.POST['exam']
            unique_id   = str(uuid.uuid4())
            staff       = Staff.objects.filter(staff_id=request.session['staff_id']).get()
            _class      = Class.objects.filter(name=class_name).get()
            students    = _class.student_set.all()
            for student in students:
                obtained_marks = 0 if mark_list[student_ids.index(student.student_id)] == '' else mark_list[student_ids.index(student.student_id)]  
                if Exam.objects.filter(name=exam, subject=subject, student=student).exists():               # If test results already exists then update existing one
                    old_record = Exam.objects.filter(name=exam, subject=subject, student=student).get()
                    old_record.marks = obtained_marks
                    old_record.save()
                else:
                    new_record = Exam(name=exam, subject=subject, marks=obtained_marks, student=student)    # else create new record
                    new_record.save()
            messages.success(request, 'Results Published Successfully!')
            return redirect('exam', class_name=class_name)

        _class      = Class.objects.filter(name=class_name).get()  # _class object will be used to display student list from that class
        students    = _class.student_set.all()                     # _class gets list of all students from that class
        staff       = Staff.objects.filter(staff_id=request.session['staff_id']).get()
        subjects    = _class.subjects.all()
        classes     = staff.classes.all()                          # classes if a list of classes to display in Attendance section if cc
        context     = {
            'staff'     : staff,
            'classes'   : classes,
            'students'  : students,
            'class'     : _class,
            'subjects'  : subjects,
            'cc'        : True
        }
        return render(request, 'staff/exam.html', context)
    else:
        return redirect('/')


def logout(request):

    student = False
    if request.session['user_type'] == 'student':
        student = True
        
    for key in list(request.session.keys()):
        del request.session[key]

    return redirect('/' if student else 'staff')