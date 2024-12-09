from django.shortcuts import render,redirect
from django.http import JsonResponse
from .views import getuserData,errorView
from requests import post
base_url = f""

def get_base_path(request):
    global base_url
    if base_url == "":
        base_url = f"http://{request.get_host()}"
        return

def render_created_task(request,task,user_data):
    task['tags'] = [tag['name'] for tag in task['tags']]
    
    context = {
        'task':task,
        'user_data':user_data
    }
    return render(request,'aigeneratedoutput.html',context)

def aigenerate(request):
    get_base_path(request)
    if request.user.is_authenticated:
        user_data = getuserData(request)
        if request.method == "POST":
            headers = {"userId":request.user.email}
            data = {"user_request":request.POST['query']}
            response = post(f"{base_url}/ai/generateTask/",headers=headers,json = data)
            if response.status_code==200:
                return render_created_task(request,response.json(),user_data)
            else:
                return errorView(request,response)
        context = {'user_data':user_data}
        return render(request = request,template_name='aigenerate.html',context=context)