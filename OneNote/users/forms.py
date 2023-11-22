from .models import OneNoteUser
from django.contrib.auth.forms import UserCreationForm

class OneNoteUserForm(UserCreationForm):
    class Meta:
        model = OneNoteUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']