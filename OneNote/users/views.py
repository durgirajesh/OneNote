from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm


from .forms import OneNoteUserForm
import json
from tasks import *

@csrf_exempt
def signup_view(request):

    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Cannot Unmarshall Content'}, status=400)
        
        form = OneNoteUserForm(json_data)
        if form.is_valid(): 
            user = form.save()
            return JsonResponse({'message': 'success'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid JSON data', 'details':form.errors}, status=400)
    
    return JsonResponse({'error' : 'Method Not allowed'}, status=405)

@csrf_exempt
def login_view(request):

    if request.user.is_authenticated:     
        return JsonResponse({'message':'User is Already authenticated'}, status=200)
    
    try:
        json_tree = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError :
        return JsonResponse({'error':'Cannot Unmarshall Content'}, status=400)
    
    loginform = AuthenticationForm(request, json_tree)
    if loginform.is_valid():
        username = loginform.cleaned_data['username']
        password = loginform.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return JsonResponse({'message':'success'}, status=200)
        else:
            return JsonResponse({'error': loginform.errors}, status=400)
        

    return JsonResponse({'error':'Bad request', 'details': 'Method not allowed'}, status=400)
