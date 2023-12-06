from django.shortcuts import render
from django.http import JsonResponse
from .forms import TaskForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core import serializers

from users.models import OneNoteUser
from .models import TasksList

# @csrf_exempt
# def create_task(request):    
#     if not request.user.is_authenticated :
#         return JsonResponse({'error': 'user not logged in'}, status = 400)
    
#     try :
#         json_data = json.loads(request.body.decode('utf-8'))
#     except :
#         return JsonResponse({'error':'Cannot Unmarshall Content'}, status=400)
    
#     form = TaskForm(json_data)
#     if form.is_valid():
        
#         task = form.save(commit=False)
#         task.user = request.user
#         task.save()

#         return JsonResponse({'message':'success', 'Data' : { 'username' : form.cleaned_data['user'].username,
#                                                             'Description' : form.cleaned_data['description']}}, status=200)
#     else:
#         return JsonResponse({'error': form.errors}, status=400)
    
    
@csrf_exempt
@login_required
def list_view(request):

    if request.method == 'GET':
        user_id = request.GET.get('user', None)
        
        if user_id is not None:
            tasks = TasksList.objects.filter(user=user_id)
            tasks_response = []
            for task in tasks:
                tasks_list = {
                    'title' : task.title,
                    'description' : task.description
                }
                tasks_response.append(tasks_list)

            context = {
                'id' : user_id,
                'tasks' : tasks_response
            }

            return JsonResponse(context)
        else:
            return JsonResponse({'message' : 'user not present'})
        
    elif request.method == 'POST':
        try :
            json_tree = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error' : 'Cannot Unmarshall content'})
        
        task_form = TaskForm(json_tree)

        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.save()
            return JsonResponse({'message' : 'success'})
        
        else:
            return JsonResponse({'error' : task_form.errors}, status=400)
        

    
