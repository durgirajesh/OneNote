from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_view, name='list_view'),
    path('update', views.update_view, name='update_view')
]