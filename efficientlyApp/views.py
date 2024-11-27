from django.shortcuts import render,redirect
from django.http import JsonResponse
from .utils import parse
import requests
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import CustomUser
import json
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.middleware.csrf import get_token

base_url = f""

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('listtasks')
        else:
            error = "Invalid email or password."
    return render(request, 'login.html', {'error': error})

def registration(request):
    get_base_path(request)
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        errors = []
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Invalid email format.")
        if password1 != password2:
            errors.append("Passwords do not match.")
        else:
            try:
                validate_password(password1)
            except ValidationError as e:
                errors.extend(e.messages)
        if CustomUser.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        if CustomUser.objects.filter(email=email).exists():
            errors.append("Email already registered.")

        if errors:
            return render(request, 'register.html', {
                'error': errors,
                'email': email,
                'username': username
            })
        try:
            user = CustomUser.objects.create_user(email=email, username=username, password=password1)
            headers = {"userId": email}
            path = f"{base_url}/data/register/"
            res = requests.post(path, headers=headers)
            if res.status_code == 200:
                login(request, user)
                return redirect('profileView')
            else:
                errors.append("Error occurred. Please register again.")
        except Exception as e:
            errors.append(str(e))

        return render(request, 'register.html', {'error': errors, 'email': email, 'username': username})

    return render(request, 'register.html')

def profile_view(request):
    get_base_path(request)
    if request.user.is_authenticated:
        if request.method == "POST":
            bio = request.POST.get("bio", "")
            profile_image = request.FILES.get("profile_image")
            commitments = request.POST.getlist("commitments[][name]")
            commitment_times = request.POST.getlist("commitments[][time]")

            if profile_image:
                request.user.profile_pic = profile_image
            request.user.save()

            data = {
                "bio": bio,
                "commitments": [{"name": name, "time": time} for name, time in zip(commitments, commitment_times)],
            }

            headers = {'userId': request.user.email}
            requests.post(f"{base_url}/data/v2/additionalInfo/", json=data, headers=headers)
            return redirect("listtasks")

        headers = {"userId": request.user.email}
        response = requests.get(f"{base_url}/data/v2/additionalInfo/", headers=headers)
        additional_info = response.json()
        profile_image = request.user.profile_pic.url if request.user.profile_pic else "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Avatar_icon_green.svg/2048px-Avatar_icon_green.svg.png"


        user_data = {
            "username": request.user.username,
            "email": request.user.email,
            "bio": additional_info.get("bio", ""),
            "profile_image": profile_image,
            "commitments": additional_info.get("commitments", []),
        }

        return render(request, 'profile.html', {"user_data": user_data})
    return redirect('login')

def logoutView(request):
    logout(request)
    return redirect('login')

def get_base_path(request):
    global base_url
    if base_url == "":
        base_url = f"http://{request.get_host()}"
        return

def getuserData(request):
        get_base_path(request)
        headers = {"userId": request.user.email}
        profile_image = request.user.profile_pic.url if request.user.profile_pic else "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Avatar_icon_green.svg/2048px-Avatar_icon_green.svg.png"
        return {"profile_image":profile_image,
                "email":request.user.email,
                "username":request.user.username}

def createtask(request):
    get_base_path(request)
    if request.user.is_authenticated:
        if request.method == 'POST':
            csrf_cookie = get_token(request)
            print(csrf_cookie)
            headers = {
                'userId': request.user.email,
            }
            json_data = parse(request)
            res = requests.post(f"{base_url}/data/v2/tasks/create/", headers=headers, json=json_data)
            if res.status_code == 200:
                return redirect('listtasks')
            else:
                return JsonResponse(res.json())
        data = {'user_data': getuserData(request)}
        return render(request, 'createTask.html', context=data)
    else:
        return redirect("login")

def listtasks(request):
    get_base_path(request)
    if request.user.is_authenticated:
        headers = {
            "userId":request.user.email
        }
        headers = {"userId": request.user.email}
        user_data = getuserData(request)
        tasks = dict(requests.get(f"{base_url}/data/v2/tasks/list/",headers=headers).json())
        data = {}
        data['tasks'] = tasks['tasks']
        for index,task in enumerate(data['tasks']):
            task['id'] = task.pop('_id')
            data["tasks"][index] = task
        data['user_data'] = user_data
        return render(request,'home.html',context = data)
    else:
        return redirect('login')

def deletetask(request,taskId):
    get_base_path(request)
    if request.user.is_authenticated:
        headers = {'userId':request.user.email}
        res = requests.delete(f"{base_url}/data/v2/tasks/{taskId}/",headers=headers)
        if res.status_code == 200:
            return redirect('listtasks')
        else:
            return JsonResponse(res.json())
    else:
        return redirect('login')
    
def updatetask(request,taskId):
    get_base_path(request)
    if request.user.is_authenticated:
        headers = {
                "userId":request.user.email
            }
        if request.method == "POST":
            get_base_path(request)
            dictData = parse(request)
            requests.put(f"{base_url}/data/v2/tasks/{taskId}/",
                          json = dictData,
                          headers=headers)
            return redirect('listtasks')
        res = requests.get(f"{base_url}/data/v2/tasks/{taskId}",headers = headers)
        context = {'task':res.json()['task'],'user_data':getuserData(request)}
        return render(request,'taskView.html',context=context)
    else:
        return redirect("login")



