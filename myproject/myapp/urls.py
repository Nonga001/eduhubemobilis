from django.urls import path
from . import views  # Import your app's views

urlpatterns = [
    path('register/', views.register, name='register'),  # Register route
    path('login/', views.login_view, name='login'),      # Login route
    path('logout/', views.logout_view, name='logout'),  # Logout route
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('courses/', views.courses_view, name='courses'),
    path('lecturers/', views.lecturers_view, name='lecturers'),
    path('contacts/', views.contacts_view, name='contacts'),
]
