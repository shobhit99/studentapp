from django import forms
from .strings import *

class StudentRegister(forms.Form):
    
    first_name = forms.CharField(max_length=20,widget=forms.TextInput(
        attrs={
            'type' : 'text',
            'class' : 'form-control',
            'placeholder' : 'First Name'
        }))

    last_name = forms.CharField(max_length=30,widget=forms.TextInput(
        attrs={
            'type' : 'text',
            'class' : 'form-control',
            'placeholder' : 'Last Name'
            }))

    email = forms.CharField(max_length=30,widget=forms.TextInput(
        attrs={
            'type' : 'email',
            'class' : 'form-control',
            'placeholder' : 'Email'
            }))

    password = forms.CharField(widget=forms.TextInput(
        attrs={
            'type' : 'password',
            'class' : 'form-control',
            'placeholder' : 'Password',
            'minlength' : '8'
            }))

    repeat_password = forms.CharField(widget=forms.TextInput(
        attrs={
            'type' : 'password',
            'class' : 'form-control',
            'placeholder' : 'Repeat Password',
            'minlength' : '8'
            }))

    student_id = forms.CharField(widget=forms.TextInput(
        attrs={
            'type' : 'text',
            'class' : 'form-control',
            'placeholder' : 'Student ID',
            'minlength' : '5'
            }))
    
    year = forms.CharField(widget=forms.Select(choices=YEARS, 
        attrs={
            'class' : 'form-control custom-select'
            }))

    section = forms.CharField(widget=forms.TextInput(
        attrs={
            'type' : 'number',
            'class' : 'form-control',
            'placeholder' : 'Section'
            }))

    gender = forms.CharField(widget=forms.Select(choices=GENDER, 
        attrs={
            'class' : 'form-control custom-select'
            }))
            
    departments = forms.CharField(widget=forms.Select(choices=DEPARTMENTS, 
        attrs={
            'class' : 'form-control custom-select'
        }))

class StudentLogin(forms.Form):

    user_login = forms.CharField(widget=forms.TextInput(
        attrs={
            'type' : 'text',
            'class' : 'form-control',
            'placeholder' : 'Student ID'
            }))

    user_password = forms.CharField(widget=forms.TextInput(
        attrs={
            'type' : 'password',
            'class' : 'form-control',
            'placeholder' : 'Password'
            }))