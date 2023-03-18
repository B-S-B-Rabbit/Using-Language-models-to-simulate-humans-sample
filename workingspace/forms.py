from django import forms

# forms.py
from django import forms

class ProjectForm(forms.Form):
    project_input = forms.CharField(help_text="Enter something", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'project_input'}))
