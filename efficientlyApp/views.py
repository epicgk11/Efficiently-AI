from django.shortcuts import render,redirect
from django.http import JsonResponse
from .utils import parse
import requests
from .forms import CustomUserRegistrationForm
from django.contrib.auth import login,authenticate
from django.contrib import messages

base_url = f""

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('listtasks')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def registration(request):
        if request.method == "POST":
            form = CustomUserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
        form = CustomUserRegistrationForm()
        return render(request,'register.html',context = {'form':form})
def get_base_path(request):
    global base_url
    if base_url == "":
        base_url = f"http://{request.get_host()}"
        return
    
def createtask(request):
    if request.method == 'POST':
        get_base_path(request)
        json_data = parse(request)
        res = requests.post(f"{base_url}/data/create/",json = json_data)
        if res.status_code == 200:
            return redirect('listtasks')
        else:
            return JsonResponse({"message":"Error Occured"})
    return render(request, 'createTask.html')

def listtasks(request):
    get_base_path(request)
    tasks = dict(requests.get(f"{base_url}/data/list").json())
    context = {"tasks":tasks['tasks']}
    return render(request,'home.html',context)

def deletetask(request,taskId):
    get_base_path(request)
    res = requests.delete(f"{base_url}/data/delete/{taskId}/")
    if res.status_code == 200:
        return redirect('listtasks')
    else:
        return JsonResponse({"message":"Error occured"})
    
def updatetask(request,taskId):
    if request.method == "POST":
        get_base_path(request)
        dictData = parse(request)
        requests.post(f"{base_url}/data/update/{taskId}/",json = dictData)
        return redirect('listtasks')
    res = requests.get(f"{base_url}/data/get/{taskId}")
    context = {'task':res.json()['task']}
    return render(request,'taskView.html',context=context)