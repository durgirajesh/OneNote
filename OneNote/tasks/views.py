from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404

from users.models import OneNoteUser
from .models import TasksList, Task
from .forms import TaskListForm, TaskForm
import json
from django.urls import path    



@csrf_exempt
@login_required 
def list_view(request):
    if request.method == 'GET':
        user_id = request.GET.get('user', None)
        
        if user_id is not None:
            user = OneNoteUser.objects.get(username=user_id)
            tasks_list = TasksList.objects.filter(user=user)

            if tasks_list:
                context = {
                    'username' : user_id,
                    'tasks' : []
                }
                for task_list in tasks_list :
                    for task in task_list.tasks.all():
                        task_data = {
                            'title' : task.title,
                            'description' : task.description
                            }
                        context['tasks'].append(task_data)
                return JsonResponse(context)
            else:
                return JsonResponse({'username' : user_id, 'message':'Tasks List Not Found For User'}, status=404)
            
        else:
            return JsonResponse({'message':'User Not Found'}, status=404)
        
    elif request.method == 'POST':
        try :
            json_tree = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error' : 'Cannot Unmarshall content'})
        
        user = OneNoteUser.objects.get(username = json_tree['user'])
        json_tree['user'] = user
        task_list_form = TaskListForm(json_tree)

        if task_list_form.is_valid():
            task_list = task_list_form.save()

            for task_data in json_tree.get('tasks', []):
                task_form = TaskForm(task_data)
                if task_form.is_valid():
                    task = task_form.save()
                    task_list.tasks.add(task)
                else:
                    return JsonResponse({'error':task_form.errors}, status=400)
            return JsonResponse({'message' : 'success'}, status=200)
        else:
            return JsonResponse({'error' : task_list_form.errors}, status=400)   

@csrf_exempt
@login_required
def update_view(request):
    if request.method == 'PUT':
        user_id= request.GET.get('user', None)
        task_title = request.GET.get('title', None)
        task_description = request.GET.get('description', None)

        if user_id is not None and task_title is not None and task_description is not None :
            user = OneNoteUser.objects.get(username = user_id)
            tasks_list = TasksList.objects.filter(user=user)

            for task_list in tasks_list:
                for task in task_list.tasks.all() : 
                    if task.title == task_title :
                        task.description = task_description
                        task.save()
            return JsonResponse({'message' : 'success'}, status=200)
        else:
            return JsonResponse({'message' : 'Invalid Parameters'}, status = 400)
        
    else:
        return JsonResponse({'message' : 'Invalid Request'}, status=405)


def delete_view(request):
    if request.method == 'DELETE':
        user_id= request.GET.get('user', None)
        task_title = request.GET.get('title', None)

        if user_id is not None and task_title is not None :
            user = OneNoteUser.objects.get(username = user_id)
            tasks_list = TasksList.objects.filter(user=user)

            for task_list in tasks_list:
                for task in task_list.tasks.all() : 
                    if task.title == task_title :
                        task.delete()
            return JsonResponse({'message' : 'success'}, status=200)
        else:
            return JsonResponse({'message' : 'Invalid Parameters'}, status = 400)
        
    else:
        return JsonResponse({'message' : 'Invalid Request'}, status=405)
    


