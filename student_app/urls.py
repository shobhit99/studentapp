from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('staff/', views.staff, name='staff'),
    path('logout/', views.logout, name='logout')
]