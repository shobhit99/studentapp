from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('staff/', views.staff, name='staff'),
    path('attendance/<class_name>', views.attendance, name='attendance'),
    path('profile/', views.profile, name='profile'),
    path('attendance/', views.student_attendance, name='student_attendance'),
    path('notice/', views.notice, name='student_notice'),
    path('notice/<action>', views.notice, name='notice'),
    path('logout/', views.logout, name='logout')
]