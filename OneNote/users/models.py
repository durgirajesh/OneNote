from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

class OneNoteUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=16)

OneNoteUser._meta.get_field('groups').remote_field.related_name = 'customuser_groups'
OneNoteUser._meta.get_field('user_permissions').remote_field.related_name = 'customuser_user_permissions'
