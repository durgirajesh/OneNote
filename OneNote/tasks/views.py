from django.shortcuts import render
from django.http import JsonResponse
from .forms import TaskForm
from django.views.decorators.csrf import csrf_exempt
import json

from users.models import OneNoteUser

@csrf_exempt
def list_view(request):    
    if not request.user.is_authenticated :
        return JsonResponse({'error': 'user not logged in'}, status = 400)
    
    try :
        json_data = json.loads(request.body.decode('utf-8'))
    except :
        return JsonResponse({'error':'Cannot Unmarshall Content'}, status=400)
    
    form = TaskForm(json_data)
    print(form)
    
    if form.is_valid():
        print(request.user)
        task = form.save(commit=False)
        task.user = form.cleaned_data['user']
        task.save()

        return JsonResponse({'message':'success'}, {'Data' : form.cleaned_data}, status=200)
    else:
        return JsonResponse({'error': form.errors}, status=400)
    
    