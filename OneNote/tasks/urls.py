from django.urls import path
from . import views

urlpatterns = [
    # path(' ', views.create_task, name='create_task'),
    path('', views.list_view, name='list_view')
]