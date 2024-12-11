# accounts/views.py
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
import django.contrib.auth
from django.contrib.auth.forms import AuthenticationForm
from pyexpat.errors import messages
from django.contrib import messages
from .forms import CourseForm
from .admin import Activity
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Course, Enrollment, Activity
from django.contrib import messages
from .models import ContactMessage
from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            django.contrib.auth.login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def about(request):
    return render(request, 'about.html')  # Your About page view

@login_required
def courses(request):
    # Get all courses (this will be visible to admin users)
    courses = Course.objects.all()

    # Get courses that the user is enrolled in
    enrolled_courses = Course.objects.filter(enrollment__user=request.user)

    # Check if the logged-in user is a lecturer
    is_lecturer = request.user.groups.filter(name='Lecturer').exists()

    if is_lecturer:
        # If the user is a lecturer, show only the courses they are teaching
        courses = Course.objects.filter(instructor=request.user)

    if request.method == "POST":
        # Handle adding or deleting courses
        if 'add_course' in request.POST:
            # Add a new course
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                course.instructor = request.user  # Set the logged-in user as the instructor
                course.save()
                return redirect('courses')  # Redirect to the course list after adding
        elif 'delete_course' in request.POST:
            # Delete a course
            course_id = request.POST.get('course_id')
            course = Course.objects.get(id=course_id)
            if course.instructor == request.user:
                course.delete()
            return redirect('courses')

    # Prepare the form for adding a new course
    form = CourseForm()

    return render(request, 'courses.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
        'is_lecturer': is_lecturer,
        'form': form  # Pass the form to the template
    })
def lecturers(request):
    lecturers = User.objects.filter(groups__name='Lecturer')  # Modify as needed based on your model structure
    return render(request, 'lecturers.html', {'lecturers': lecturers})


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save to the database
        contact_message = ContactMessage(name=name, email=email, message=message)
        contact_message.save()

        # Email subject and body
        subject = f"Contact Form Submission from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            # Send email
            send_mail(
                subject,
                body,
                email,  # Sender's email (dynamic)
                ['nongashaldon@gmail.com'],  # Fixed recipient's email
                fail_silently=False,
            )
            # Add success message
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
            messages.error(request, "An error occurred while sending the email. Please try again later.")

        return redirect('contacts')

    return render(request, 'contacts.html')

def course_list(request):
    if request.user.groups.filter(name='Lecturer').exists():
        # Only show courses for the logged-in lecturer
        courses = Course.objects.filter(instructor=request.user)
    else:
        courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})
# View to handle course enrollment
@login_required
def enroll(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, "The course you are trying to enroll in does not exist.")
        return redirect('courses')

    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, "You are already enrolled in this course.")
    else:
        Enrollment.objects.create(user=request.user, course=course)
        Activity.objects.create(user=request.user, action=f"Enrolled in {course.title}")
        messages.success(request, f"You have successfully enrolled in {course.title}.")

    return redirect('courses')

def home(request):
    # Get the enrolled courses
    enrolled_courses = Enrollment.objects.filter(user=request.user)

    # Get the activities of the logged-in user
    activities = Activity.objects.filter(user=request.user).order_by('-timestamp')

    return render(request, 'home.html', {
        'enrolled_courses': enrolled_courses,
        'activities': activities
    })

@login_required
def unenroll(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, "The course you are trying to unenroll from does not exist.")
        return redirect('courses')

    enrollment = Enrollment.objects.filter(user=request.user, course=course)
    if enrollment.exists():
        enrollment.delete()
        Activity.objects.create(user=request.user, action=f"Unenrolled from {course.title}")
        messages.success(request, f"You have successfully unenrolled from {course.title}.")
    else:
        messages.info(request, "You are not enrolled in this course.")

    return redirect('courses')


@login_required
def activity_log(request):
    activities = Activity.objects.filter(user=request.user).order_by('-timestamp')  # Most recent first
    return render(request, 'activity_log.html', {'activities': activities})
def add_course(request):
    if not request.user.groups.filter(name='Lecturer').exists():
        return redirect('courses')  # Or any other page for non-lecturers

    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user  # Set the logged-in user as the instructor
            course.save()
            return redirect('courses')  # Redirect to the course list after adding
    else:
        form = CourseForm()

    return render(request, 'add_course.html', {'form': form})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user == course.instructor:
        course.delete()
    return redirect('courses')


class Lecturer:
    pass




def logout_view(request):
    logout(request)
    return redirect('login')