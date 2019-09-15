from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import *
from .methods import *
import uuid

# Create your views here.
def index(request):

    if 'user_type' in request.session.keys():                       # redirect to profile if logged in
            return redirect('profile')

    register_form  = StudentRegister()
    login_form     = StudentLogin()
    context = {'register_form' : register_form, 'login_form' : login_form }

    if request.method == 'POST':
        if 'login-form' in request.POST:                            # If login request

            login_form = StudentLogin(request.POST)                 # Get object of login form
            
            if login_form.is_valid():
                
                if Student.objects.filter(student_id=request.POST['user_login']).exists():        # If given user id exists then check for password
                    student = Student.objects.filter(student_id=request.POST['user_login'])[0]
                    if check_password(request.POST['user_password'], student.password):

                        for key in list(request.session.keys()):                                   # Delete previous sessions if any
                            del request.session[key]

                        request.session['user_type'] = 'student'                                   # user_type in session variable will decide contents
                        request.session['student_id'] = student.student_id
                        return redirect('profile')                                                 # redirect to profile page after login
                    else:
                        messages.error(request, 'Login ID or password incorrect')
                        return redirect('/')
                else:
                    messages.error(request, 'Login ID or password incorrect')
                    return redirect('/')
                
        elif 'register-form' in request.POST:                       # If register request
            
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
                    context['register_msg'] = True
                    return render(request, 'student_app/index.html', context)                        # If passwords don't match or email / student id already registered display error

                hashed_password = make_password(request.POST['password'], salt=None, hasher='default')
                department  = Department.objects.filter(name=request.POST['departments']).get()                 # department is foregin key in Student table
                _class      = Class.objects.filter(name=request.POST['year']+request.POST['section']).get()     # class is a foreign key in class table
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
                context['register_msg'] = True                                  # Switch to register form if messages are related to register form
                return render(request, 'student_app/index.html', context)  

    return render(request, 'student_app/index.html', context)


def staff(request):

    if 'user_type' in request.session.keys():                       # redirect to profile if logged in
            return redirect('profile')

    register_form  = StaffRegister()
    login_form     = StaffLogin() 
    context = {'register_form' : register_form, 'login_form' : login_form }

    if request.method == 'POST':
        if 'login-form' in request.POST:

            login_form = StaffLogin(request.POST)
            
            if login_form.is_valid():
                if Staff.objects.filter(staff_id=request.POST['staff_login']).exists():     # If staff id valid check password
                    staff = Staff.objects.filter(staff_id=request.POST['staff_login'])[0]
                    if check_password(request.POST['staff_password'], staff.password):

                        for key in list(request.session.keys()):                            # Delete previous session if any
                            del request.session[key]
                        
                        request.session['user_type'] = 'staff'                              # user type will decide contents
                        request.session['staff_id']  = staff.staff_id                       # save staff_id in sessions to get staff object later
                        return redirect('profile')
                    else:
                        messages.error(request, 'Login ID or password incorrect')           # if wrong user / pass combination display error
                        return redirect('staff')
                else:
                    messages.error(request, 'Login ID or password incorrect')
                    return redirect('/')
                

        elif 'register-form' in request.POST:                                               # If request for registration
            
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
                    context['register_msg'] = True                                # Switch to register form if messages are related to register form
                    return render(request, 'staff/index.html', context)           # If passwords don't match or id / email already registered then display errors                           

                hashed_password = make_password(request.POST['password'], salt=None, hasher='default')
                department  = Department.objects.filter(name=request.POST['departments']).get()     # department is foreign key in Staff table
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
                context['register_msg'] = True                                      # Switch to register form if messages are related to register form
                return render(request, 'staff/index.html', context)

    return render(request, 'staff/index.html', context)


def profile(request):
    
    if 'user_type' not in request.session.keys():                   # if not logged in then redirect to home page
        return redirect('/')

    if request.session['user_type'] == 'student':                   # if user is student then display student's profile
        context = student_context(request.session['student_id'])
        return render(request, 'student_app/profile.html', context)

    elif request.session['user_type'] == 'staff':                   # if user is staff then display staff's profile
        context = staff_context(request.session['staff_id'])
        request.session['cc'] = context['cc']                       # if teaching staff then "Attendance" menu will be visible if librarian then books
        return render(request, 'staff/profile.html', context)


def books(request, action='view'):

    if 'user_type' not in request.session.keys():                       # if not logged in then redirect to home page   
        return redirect('/')
    
    if request.session['user_type'] == 'student':                       # if user is student then display borrowed books
        context         = student_context(request.session['student_id'])
        return render(request, 'student_app/books.html', context)

    elif request.session['user_type'] == 'staff':                       # if user is staff and librarian then show menu with add, delete, lend, return options
        context = staff_context(request.session['staff_id'])

        if action == 'add_record':
            if "search" in request.POST:                                # Return matching books
                book_name = request.POST['book_name']
                results   = Book.objects.filter(name__contains=book_name) if Book.objects.filter(name__contains=book_name).count() else False
                if not results:
                    messages.success(request, "No Records found")       # No books found with given name
                else:
                    context['search'] = True
                    context['books']  = results
                    return render(request, 'staff/add-record.html', context)
                return redirect('books', action='add_record')

            elif "lend" in request.POST:                                # Add borrow record
                student_id = request.POST['student_id']
                isbn       = request.POST['isbn']

                if Student.objects.filter(student_id=student_id).exists() and Book.objects.filter(isbn=isbn).exists():      # If given student and book exists
                    student = Student.objects.filter(student_id=student_id).get()
                    book    = Book.objects.filter(isbn=isbn).get()
                else:
                    messages.error(request, "Invalid ISBN or Student ID")
                    return redirect('books', action='add_record')

                new_borrow_record = BorrowRecord(student=student, book=book)    # Add borrowed book record
                new_borrow_record.save()
                messages.success(request, "Success !")
                return redirect('books', action='add_record')


            return render(request, 'staff/add-record.html', context)
        
        elif action == "delete_record":                                         # if book is returned by student delete the borrow record
            if "search" in request.POST:
                if Student.objects.filter(student_id=request.POST['student_id']).exists():          # if given student_id exists
                    student = Student.objects.filter(student_id=request.POST['student_id']).get()   # get student object
                else:
                    messages.error(request, "Invalid Student ID")
                    return redirect('books', action='delete_record')
                borrowed_books = student.borrowrecord_set.all()                 # get list of borrowed books by student
                results = True if borrowed_books.count() else False             # if borrowed books > 1 then results = True else False
                if not results:
                    messages.error(request, "No records found")                 # if count is 0
                    return redirect('books', action='delete_record')
                context['borrowed_books'] = borrowed_books
                context['search']         = True
                return render(request, 'staff/delete-record.html', context)
            
            elif "return" in request.POST:                                      # when book is marked as returned
                returned_books = request.POST.getlist('book_list[]')            # get the list of books returned by student
                for b in returned_books:
                    book = BorrowRecord.objects.filter(id=b)
                    book.delete()                                               # delete borrow record
                messages.success(request, "Books marked as returned")
                return redirect('books', action='delete_record')


            return render(request, 'staff/delete-record.html', context)

        elif action == "add":                       # Add books to database   
            if request.method == "POST":
                book_name = request.POST['book_name']
                isbn      = request.POST['isbn']
                new_book  = Book(name=book_name, isbn=isbn)
                new_book.save()
                messages.success(request, "Book added to Database!")
                return redirect('books', action='add')
            return render(request, 'staff/add-book.html', context)

        elif action == "view":                     # View books in database
            books   = Book.objects.all()
            context['books'] = books
            return render(request, 'staff/view-books.html', context)
    

def notice(request, action='view'):
    
    if 'user_type' not in request.session.keys():
        return redirect('/')
    
    if request.session['user_type'] == 'student':                                   # if student then get the list of notices of his/her class
        context             = student_context(request.session['student_id'])
        no_notice           = True if context['student']._class.notice_set.all().count() == 0 else False        # if no notice added by any teacher
        if no_notice:
            context['notices'] = no_notice
        else:
            context['notices']  = context['student']._class.notice_set.all().order_by('-id')[:10]   # get the last 10 notices
        return render(request, 'student_app/notice.html', context)

    elif request.session['user_type'] == 'staff':                                   # If user is staff then he/she will be able to add and view notices
        context = staff_context(request.session['staff_id'])
        request.session['cc'] = context['cc']
        if request.session['cc'] == True:
            staff       = Staff.objects.filter(staff_id=request.session['staff_id']).get()
            classes     = staff.classes.all()
            notices     = staff.notice_set.all().order_by('-id')[:10]
            context = {
                'staff'   : staff,
                'classes' : classes,
                'notices' : notices,
                'cc' : True
            }
            
            if action == 'view':                                                    # show all the notices added by current staff
                if request.method == "POST":                                        # POST method is called when pressed on delete
                    noteid  = request.POST['id']
                    Notice.objects.filter(pk=noteid).delete()
                    messages.success(request, "Notice Deleted!")
                    return redirect('notice', action='view')
                return render(request, 'staff/view-notice.html', context)
                
            else:                                                                   # delete the notice
                if request.method == "POST":                                        # adding the notice

                    title      = request.POST['title']
                    notice     = request.POST['notice']
                    class_list = request.POST.getlist('class_list[]')

                    notice = Notice(title=title, notice=notice, added_by=staff)     
                    notice.save()                                                   # notice added
                    for class_name in class_list:
                        c = Class.objects.filter(name=class_name).get()
                        notice.class_obj.add(c)                                     # add notice to all the classes checked by staff
                    messages.success(request, "Notice Added!")
                    return redirect('notice', action='add')
                
                return render(request, 'staff/add-notice.html', context)
        else:
            return redirect('/')


def attendance(request, class_name):

    if 'user_type' not in request.session.keys():
        return redirect('/')

    if request.session['cc'] == True:                                               # If teaching staff then process the request else redirect
        if request.method == "POST":
            values      = request.POST.getlist('student_list[]')
            subject     = Subject.objects.filter(name=request.POST['subject']).get()
            unique_id   = str(uuid.uuid4())                                         # generate unique randomg string for current attendance instance
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
        classes     = staff.classes.all()                          # classes is a list of classes to display in Attendance section if teaching staff
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
        subject_count = 0
        for subject in subjects:
            total           = Attendance.objects.filter(student=student).filter(subject=subject).count()                        # total lectures conducted
            attended        = Attendance.objects.filter(student=student).filter(subject=subject).filter(status=True).count()    # total lectures attended by student
            percent         = 0 if not total else (attended/total)*100                                                          # Avoid division if total is zero
            if total:
                subject_count += 1
            percent_count += percent
            attendance[subject.name] = [
                total, 
                attended,
                "{:.2f}".format(percent)
            ]
        avg_attendance = "N/A" if subject_count == 0 else (percent_count / subject_count)                          # Calculate Average attendance
        context['attendance'] = attendance
        context['avg_attendance'] = "N/A" if avg_attendance == "N/A" else "{:.2f}".format(avg_attendance)          # round number to two points
    return render(request, 'student_app/attendance.html', context)
    

def results(request):

    if request.session['user_type'] == 'student':                       # if user type is student then process request else redirect
        context   = student_context(request.session['student_id'])
        if context['student'].exam_set.filter(name='unit1').count():    # if unit1 test results are present then get the object else unit1 = False
            unit1 = context['student'].exam_set.filter(name='unit1')
        else:
            unit1 = False
        if context['student'].exam_set.filter(name='unit2').count():    # if unit2 test results are present then get the object else unit2 = False
            unit2 = context['student'].exam_set.filter(name='unit2')
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
        
    if request.session['cc'] == True:                               # if teaching staff then process request else redirect to home
        if request.method == "POST":
            student_ids = request.POST.getlist('student_list[]')    # get the list of students
            mark_list   = request.POST.getlist('mark_list[]')       # get the list of marks obtained
            subject     = Subject.objects.filter(name=request.POST['subject']).get()
            exam        = request.POST['exam']
            staff       = Staff.objects.filter(staff_id=request.session['staff_id']).get()
            _class      = Class.objects.filter(name=class_name).get()
            students    = _class.student_set.all()
            for student in students:
                obtained_marks = 0 if mark_list[student_ids.index(student.student_id)] == '' else mark_list[student_ids.index(student.student_id)]  # if empty marks consider 0
                if Exam.objects.filter(name=exam, subject=subject, student=student).exists():               # If test results already exists then update existing record
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


def update(request):

    if 'user_type' not in request.session.keys():
        return redirect('/')
    if request.session['user_type'] == 'student':
        context   = student_context(request.session['student_id'])
        if request.method == "POST":
            first_name          = request.POST['first_name']
            last_name           = request.POST['last_name']
            email               = request.POST['email']
            student             = Student.objects.filter(student_id=context['student'].student_id).get()
            student.first_name  = first_name
            student.last_name   = last_name
            student.email       = email
            student.save()                      # Save updated values
            messages.success(request, 'Profile Updated!')
            return redirect('profile')
    
    elif request.session['user_type'] == 'staff':
        context = staff_context(request.session['staff_id'])
        first_name          = request.POST['first_name']
        last_name           = request.POST['last_name']
        email               = request.POST['email']
        staff               = Staff.objects.filter(staff_id=context['staff'].staff_id).get()
        staff.first_name    = first_name
        staff.last_name     = last_name
        staff.email         = email
        staff.save()                           # Save updated values
        messages.success(request, 'Profile Updated!')
        return redirect('profile')
    
    return redirect('profile')


def logout(request):

    student = False
    if request.session['user_type'] == 'student':
        student = True
        
    for key in list(request.session.keys()):
        del request.session[key]

    return redirect('/' if student else 'staff')    # after logout redirect to / if student else /staff if staff