from django import forms
from .models import TasksList
from users.models import OneNoteUser

class TaskForm(forms.ModelForm):
    class Meta:
        model = TasksList
        fields = ['user', 'title', 'description']

    # def __init__(self, *args, **kwargs):
    #     super(TaskForm,self).__init__(*args, **kwargs)
    #     self.fields['user'].queryset = OneNoteUser.objects.all()