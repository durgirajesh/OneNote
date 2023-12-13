from django import forms
from .models import TasksList, Task
from django.forms import inlineformset_factory


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

class TaskListForm(forms.ModelForm):
    class Meta:
        model = TasksList
        fields = ['user']
