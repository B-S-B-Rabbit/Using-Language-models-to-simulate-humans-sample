from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


from django.shortcuts import render
from .forms import ProjectForm

def project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['project_input']
            # Perform some processing on the input text
            output_text = "here we can do something"
            return render(request, 'project.html', {'form': form, 'response': output_text})
    else:
        form = ProjectForm()
    return render(request, 'project.html', {'form': form})

