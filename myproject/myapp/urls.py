# accounts/urls.py
from django.shortcuts import redirect
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('myapp/', lambda request: redirect('dashboard')),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('activity-log/', views.activity_log, name='activity_log'),

    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),  # List all courses
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),  # Course detail page
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),  # Enroll in course
    path('unenroll/<int:course_id>/', views.unenroll, name='unenroll'),  # Unenroll from course  # Enroll in course
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('lecturers/', views.lecturers, name='lecturers'),
    path('contacts/', views.contacts, name='contacts'),
    path('logout/', views.logout_view, name='logout'),  # Logout URl

]

