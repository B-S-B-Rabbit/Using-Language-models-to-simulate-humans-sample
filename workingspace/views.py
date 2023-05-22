"""
This module contains views and functions for a Django web application.

"""

from django.conf import settings
from django.core.mail import send_mail
from .forms import RegisterForm, ProjectForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import URequest
from django.core.paginator import Paginator
from .API_class import API

res = API()


def home(request):
    """
    Render the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered home page.
    """
    return render(request, 'index.html')


def about(request):
    """
    Render the about page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered about page.
    """
    return render(request, 'about.html')


def project(request):
    """
    Handle the project view.

    If the request method is POST, process the form data and save a new request.
    If the form is valid, retrieve a response from the API and render the project page with the form and response.
    If the request method is GET, render the project page with an empty form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered project page.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['request_text']
            new_request = URequest(user=request.user, request_text=form.cleaned_data['request_text'])
            new_request.save()
            output_text = res.get_bot_answer(input_text)
            new_request.response_text = output_text
            new_request.save()
            return render(request, 'project.html', {'form': form, 'response': output_text})
    else:
        form = ProjectForm()
    return render(request, 'project.html', {'form': form})


def register_s_i(request):
    """
    Handle the registration view for individual users.

    If the request method is GET, render the registration form.
    If the request method is POST, process the form data and create a new user account.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered registration page.
    """
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'registration_s_i.html', context)
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Account was created for ' + username)
            subject = 'Добро пожаловать на наш сайт!'
            message = 'Уважаемый пользователь {},\nСпасибо за регистрацию на нашем сайте.'.format(username)
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [form.cleaned_data.get('email')]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return redirect('home')
    else:
        messages.error(request, 'Error Processing Your Request')
    context = {'form': form}
    return render(request, 'registration_s_i.html', context)


class MyLoginView(LoginView):
    """
    Custom login view for the application.

    Renders the login page using the specified template and form class.

    """
    template_name = 'registration_l_i.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')


class LogoutView(View):
    """
    View for handling user logout.

    Logs out the user and redirects to the login page.

    """
    def get(self, request):
        """
        Handle the GET request for user logout.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: The HTTP redirect response.

        """
        logout(request)
        return redirect('register\login')


class ProfileView(View):
    """
    View for user profile and request history.

    Renders the profile page and displays the user's request history.

    """
    def get(self, request):
        """
        Handle the GET request for the profile view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response containing the rendered profile page.

        """
        form = ProjectForm()
        user_requests = URequest.objects.filter(user=request.user).order_by('-request_date')
        paginator = Paginator(user_requests, 5)  # 10 requests per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'profile_requests.html', {'form': form, 'page_obj': page_obj})


def profile(request):
    """
    Render the user profile page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered profile page.
    """
    return render(request, 'profile.html')
