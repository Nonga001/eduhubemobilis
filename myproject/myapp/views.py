from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm


def register(request):
    # Prevent logged-in users from accessing registration
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            # Add more specific error handling
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    # Prevent logged-in users from accessing login page
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's built-in authentication with more robust error handling
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            # Add logging for failed login attempts
            # logger.warning(f'Failed login attempt for username: {username}')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    username = request.user.username
    logout(request)
    messages.success(request, f'Goodbye, {username}! You have been logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'user': request.user,
        # Add any additional context data you want to pass to the dashboard
    })

def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def courses_view(request):
    return render(request, 'courses.html')

def lecturers_view(request):
    return render(request, 'lecturers.html')

def contacts_view(request):
    return render(request, 'contacts.html')
