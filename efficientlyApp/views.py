from django.shortcuts import render,redirect
from django.http import JsonResponse
from .utils import parse
import requests


base_url = f""
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