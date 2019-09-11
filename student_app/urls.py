from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('staff/', views.staff, name='staff'),
    path('students/', views.students, name='students'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout')
]