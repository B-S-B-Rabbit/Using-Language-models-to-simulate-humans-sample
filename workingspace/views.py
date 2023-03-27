def home(request):
    return render(request, 'index.html')


from django.shortcuts import render, redirect
from .forms import ProjectForm


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
        return redirect('home')
    else:
        print('Form is not valid')
        messages.error(request, 'Error Processing Your Request')
        context = {'form': form}
        return render(request, 'registration_s_i.html', context)

