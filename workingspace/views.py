from django.conf import settings
from django.core.mail import send_mail
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import ProjectForm
from .models import URequest
from django.core.paginator import Paginator
from .API_class import API

res = API()


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['request_text']
            # Perform some processing on the input text
            new_request = URequest(user=request.user,
                                   request_text=form.cleaned_data['request_text'])
            new_request.save()
            output_text = res.get_bot_answer(input_text)
            new_request.response_text = output_text
            new_request.save()

            return render(request, 'project.html', {'form': form, 'response': output_text})
    else:
        form = ProjectForm()
    return render(request, 'project.html', {'form': form})


def register_s_i(request):
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
    template_name = 'registration_l_i.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('register\login')


class ProfileView(View):
    def get(self, request):
        form = ProjectForm()
        user_requests = URequest.objects.filter(user=request.user).order_by('-request_date')
        paginator = Paginator(user_requests, 5)  # 10 запросов на страницу
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'profile_requests.html', {'form': form, 'page_obj': page_obj})


def profile(request):
    return render(request, 'profile.html')
