from django.shortcuts import render,redirect
from django.http import JsonResponse
from .utils import parse
import requests

def createtask(request):
    if request.method == 'POST':
        base_url = f"http://{request.get_host()}"
        json_data = parse(request)
        res = requests.post(f"{base_url}/data/create/",json = json_data)
        if res.status_code == 200:
            return redirect('listtasks')
        else:
            return JsonResponse({"message":"Error Occured"})
    return render(request, 'createTask.html')

def listtasks(request):
    base_url = f"http://{request.get_host()}"
    tasks = dict(requests.get(f"{base_url}/data/list").json())
    context = {"tasks":tasks['tasks']}
    return render(request,'home.html',context)

def deletetask(request,taskId):
    base_url = f"http://{request.get_host()}"
    res = requests.delete(f"{base_url}/data/delete/{taskId}/")
    if res.status_code == 200:
        return redirect('listtasks')
    else:
        return JsonResponse({"message":"Error occured"})
    
def updatetask(request,taskId):
    if request.method == "POST":
        print(request.POST.getlist('step_completed[]'))
    base_url = f"http://{request.get_host()}"
    res = requests.get(f"{base_url}/data/get/{taskId}")
    context = {'task':res.json()['task']}
    return render(request,'taskView.html',context=context)