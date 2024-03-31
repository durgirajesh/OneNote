from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from .forms import OneNoteUserForm
from .models import OneNoteUser
import json

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
    
    if request.method == 'POST':
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
    else:
        return JsonResponse({'error':'Bad request', 'details': 'Method not allowed'}, status=400)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        username_ = request.GET.get('username', None)
        if username_ is None:
            return JsonResponse({'error': 'Invalid User'})
        else:
            try:
                user_ = OneNoteUser.objects.filter(username = username_).first()
                if username_ == str(user_) and request.user.is_authenticated:
                    logout(request)
                    return JsonResponse({'message': f'{user_.username} logged out '})
                else:
                    return JsonResponse({'message': f'{user_.username} not logged in'})
            except OneNoteUser.DoesNotExist:
                return JsonResponse({'message': f' username does not exist'})
    else:
        return JsonResponse({'message':'Invalid/Bad request'})