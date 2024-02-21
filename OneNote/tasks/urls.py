from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_view, name='list_view'), # type: ignore
    path('update', views.update_view, name='update_view')
]