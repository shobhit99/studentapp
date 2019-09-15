from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('staff/', views.staff, name='staff'),
    path('attendance/<class_name>', views.attendance, name='attendance'),
    path('profile/', views.profile, name='profile'),
    path('attendance/', views.student_attendance, name='student_attendance'),
    path('notice/', views.notice, name='student_notice'),
    path('notice/<action>', views.notice, name='notice'),
    path('results/', views.results, name='results'),
    path('exam/<class_name>', views.exam, name='exam'),
    path('books/<action>', views.books, name='books'),
    path('update/', views.update, name='update'),
    path('details/<student_id>', views.details, name='details'),
    path('logout/', views.logout, name='logout')
]