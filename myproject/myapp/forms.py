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
        fields = ['title', 'description', 'credits', 'instructor']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control', 'style': 'resize: vertical;'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius: 5px;'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'style': 'border-radius: 5px;'}),
            'instructor': forms.Select(attrs={'class': 'form-control', 'style': 'border-radius: 5px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        # Add custom inline styling to all fields
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'margin-bottom: 15px; padding: 10px; font-size: 1rem; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);'
            })