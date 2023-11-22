from django.db import models
from users.models import OneNoteUser

class TasksList(models.Model):
    user = models.ForeignKey(OneNoteUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    description = models.TextField(max_length=1000)
