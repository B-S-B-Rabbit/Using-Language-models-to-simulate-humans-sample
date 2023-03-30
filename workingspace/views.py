from django.conf import settings
from django.core.mail import send_mail



def home(request):
    return render(request, 'index.html')


from django.shortcuts import render, redirect
from .forms import ProjectForm


def about(request):
    return render(request, 'about.html')


def project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['project_input']
            # Perform some processing on the input text
            output_text = "here we can do somethin"
            return render(request, 'project.html', {'form': form, 'response': output_text})
    else:
        form = ProjectForm()
    return render(request, 'project.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm


def register_s_i(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'registration_s_i.html', context)
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request, 'Account was created for ' + user)
        subject = 'Добро пожаловать на наш сайт!'
        message = 'Уважаемый {},\nСпасибо за регистрацию на нашем сайте.'.format(user)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [form.cleaned_data.get('email')]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return redirect('home')
    else:
        print('Form is not valid')
        messages.error(request, 'Error Processing Your Request')
        context = {'form': form}
        return render(request, 'registration_s_i.html', context)


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm


class MyLoginView(LoginView):
    template_name = 'registration_l_i.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import View


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('register\login')
