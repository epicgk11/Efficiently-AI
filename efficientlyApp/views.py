from django.shortcuts import render,redirect
from django.http import JsonResponse
from .utils import parse
import requests
from .forms import CustomUserRegistrationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import CustomUser
import base64
from django.core.files.base import ContentFile
import json
base_url = f""

# Account Views

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
    print(request.user  )
    return render(request, 'login.html')

def registration(request):
    get_base_path(request)
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'register.html', {
                'error': "Passwords do not match."
            })

        try:
            user = CustomUser.objects.create_user(email=email, username=username, password=password1)
            headers = {
                "userId":email
            }
            path = f"{base_url}/data/register/"
            res = requests.post(path,headers=headers)
            if res.status_code==200:
                return redirect('profileView')
            else:
                return render(request, 'register.html', {
                    'error': "Error occured Please register again!!",
                })            
        except Exception as e:
            return render(request, 'register.html', {
                'error': str(e),
            })

    return render(request, 'register.html')

def profile_view(request):
    get_base_path(request)
    if request.user.is_authenticated:
        if request.method == "POST":
            bio = request.POST.get("bio", "")
            profile_image = request.FILES.get("profile_image")
            commitments = request.POST.getlist("commitments[][name]")
            commitment_times = request.POST.getlist("commitments[][time]")

            bs4_image_encoded = None
            if profile_image:
                # Ensure proper encoding
                file_content = profile_image.read()
                bs4_image_encoded = base64.b64encode(file_content).decode('utf-8')

            data = {
                "bio": bio,
                "profilePic": bs4_image_encoded,
                "commitments": [{"name": name, "time": time} for name, time in zip(commitments, commitment_times)],
            }

            headers = {'userId': request.user.email}
            requests.post(f"{base_url}/data/addinfo/", data=json.dumps(data), headers=headers)
            return redirect("profileView")

        headers = {"userId": request.user.email}
        response = requests.get(f"{base_url}/data/getaddinfo", headers=headers)
        additional_info = response.json().get('additional_info', {})
        profile_image = additional_info.get('image bytes', None)
        if profile_image:
            profile_image = f"data:image/png;base64,{profile_image}"
        else:
            profile_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Avatar_icon_green.svg/2048px-Avatar_icon_green.svg.png"

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



# TASKS VIEWS
def get_base_path(request):
    global base_url
    if base_url == "":
        base_url = f"http://{request.get_host()}"
        return

def getuserData(request):
        headers = {"userId": request.user.email}
        response = requests.get(f"{base_url}/data/getprofilepic/", headers=headers)
        profile_image = response.json().get('image bytes', None)
        if profile_image:
            profile_image = f"data:image/png;base64,{profile_image}"
        else:
            profile_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Avatar_icon_green.svg/2048px-Avatar_icon_green.svg.png"
        return {"profile_image":profile_image,
                "email":request.user.email,
                "username":request.user.username}

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
    if request.user.is_authenticated:
        headers = {
            "userId":request.user.email
        }
        get_base_path(request)
        headers = {"userId": request.user.email}
        user_data = getuserData(request)
        print("Gotten user data")
        tasks = dict(requests.get(f"{base_url}/data/tasks/",headers=headers).json())
        data = {}
        data['tasks'] = tasks['tasks']
        data['user_data'] = user_data
        return render(request,'home.html',context = data)
    else:
        return redirect('login')

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



