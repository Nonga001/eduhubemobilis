from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Course  # Import your Course model


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'credits', 'instructor']  # Adjust fields based on your Course model
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Customize widgets if necessary
        }

    # Optional: add custom validation or methods if needed
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Course.objects.filter(title=title).exists():
            raise forms.ValidationError("A course with this title already exists.")
        return title
