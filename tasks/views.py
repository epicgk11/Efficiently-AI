import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import re  # Import re module for regular expressions
from .parsing import parseTaskDataFromRequest
BASE_API_URL = "http://127.0.0.1:8000/data"

def listTasks(request):
    filter_params = {
        'name': request.GET.get('name', ''),
        'due_date': request.GET.get('due_date', ''),
        'tags': request.GET.get('tags', ''),
    }
    group_by = request.GET.get('group_by', '')

    response = requests.get(f"{BASE_API_URL}/list/", params=filter_params)
    tasks = response.json().get('tasks', [])
    for task in tasks:
        task['id'] = task.pop('_id', task.get('id'))

    if group_by == 'tags':
        grouped_tasks = {}
        for task in tasks:
            task_tags = task.get('tags', ['No Tag'])
            for tag in task_tags:
                grouped_tasks.setdefault(tag, []).append(task)
        context = {'grouped_tasks': grouped_tasks, 'group_by_tags': True}
    else:
        context = {'tasks': tasks}

    return render(request, 'main.html', context)

def createTask(request):
    if request.method == 'POST':
        task_data = parseTaskDataFromRequest(request)
        print(task_data)
        response = requests.post(f"{BASE_API_URL}/create/", json=task_data)
        if response.status_code == 200:
            return redirect('listtasks')
        else:
            return JsonResponse({'error': 'Failed to create task'}, status=400)
    return render(request, 'create.html')

def updateTask(request, task_id):
    if request.method == 'POST':
        task_data = parseTaskDataFromRequest(request)
        if not task_data.get('completed', False):
            response = requests.post(f"{BASE_API_URL}/update/{task_id}/", json=task_data)
        else:
            response = requests.delete(f"{BASE_API_URL}/delete/{task_id}/")
        if response.status_code == 200:
            return redirect('listtasks')
        else:
            return JsonResponse({'error': 'Failed to update task'}, status=400)
    else:
        response = requests.get(f"{BASE_API_URL}/get/{task_id}/")
        if response.status_code == 200:
            task_data = response.json()
            task_data['id'] = task_data.pop('_id', task_id)
            return JsonResponse({'task': task_data})
        else:
            return JsonResponse({'error': 'Failed to fetch task data'}, status=400)

def getTask(request, taskId):
    res = requests.get(f"{BASE_API_URL}/get/{taskId}/")
    if res.status_code == 200:
        task_data = res.json()
        task_data['id'] = task_data.pop('_id', taskId)
        return JsonResponse({'task': task_data})
    else:
        return JsonResponse({"Message": "Error occurred"}, status=400)
