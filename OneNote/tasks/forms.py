from django import forms
from .models import TasksList

class TaskForm(forms.ModelForm):
    class Meta:
        model = TasksList
        fields = ['user', 'title', 'description']