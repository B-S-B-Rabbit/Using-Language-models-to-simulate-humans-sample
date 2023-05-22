"""
This module contains Django forms used in the web application.

"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RequestForm(forms.Form):
    """
    Form for handling requests.

    Contains fields for the request text and response text.

    """
    request_text = forms.CharField(widget=forms.Textarea)
    response_text = forms.CharField(widget=forms.Textarea, required=False)


class RegisterForm(UserCreationForm):
    """
    Form for user registration.

    Inherits from UserCreationForm and adds additional fields for email and a check field.

    """
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    username = forms.CharField(
        max_length=200,
        required=True,
        help_text='Enter Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password1 = forms.CharField(
        help_text='Enter Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        required=True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )
    check = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'check']


class LoginForm(AuthenticationForm):
    """
    Form for user login.

    Inherits from AuthenticationForm and adds an additional field for username.

    """
    username = forms.CharField(
        max_length=200,
        required=True,
        help_text='Enter Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )

    password = forms.CharField(
        help_text='Enter Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class ProjectForm(forms.Form):
    """
    Form for handling project requests.

    Contains fields for the request text and response text.

    """
    request_text = forms.CharField(
        help_text="Enter something",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'project_input'}),
    )
    response_text = forms.CharField(widget=forms.Textarea, required=False)
