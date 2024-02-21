from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.list_view, name='list_view'), # type: ignore
    path('update', views.update_view, name='update_view')
=======
    path('', views.list_view, name='list_view'),
    path('update', views.update_view, name='update_view'),
    path('delete', views.delete_view, name='delete_view')
>>>>>>> 545d61fcc295fc883899ad807bd299f036e1808e
]