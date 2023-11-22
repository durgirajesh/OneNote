from django.shortcuts import render
from django.http import JsonResponse
from .forms import TaskForm
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def list_view(request):    
    if not request.user.is_authenticated :
        return JsonResponse({'error': 'user not logged in'}, status = 400)
    
    try :
        json_data = json.loads(request.body.decode('utf-8'))
    except :
        return JsonResponse({'error':'Cannot Unmarshall Content'}, status=400)
    
    form = TaskForm(json_data)
    if form.is_valid():
        task = form.save()
        task.user = request.user()
        task.save()

        return JsonResponse({'message':'success'}, {'form' : form}, status=200)
    else:
        return JsonResponse({'error': form.errors}, status=400)
    
    