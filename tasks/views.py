import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

BASE_API_URL = "http://127.0.0.1:8000/data" 

def listTasks(request):
    response = requests.get(f"{BASE_API_URL}/list/")
    tasks = response.json().get('tasks', [])
    return render(request, 'main.html', {'tasks': tasks})


def createTask(request):
    if request.method == 'POST':
        task_name = request.POST.get('name')
        task_description = request.POST.get('description')
        task_due_date = request.POST.get('due_date')
        task_resources = request.POST.get('resources', '')
        task_tags = request.POST.getlist('tags')
        steps = []
        for key in request.POST.keys():
            if key.startswith('step-') and key.endswith('-name'):
                step_index = key.split('-')[1]
                steps.append({
                    'name': request.POST.get(f'step-{step_index}-name'),
                    'description': request.POST.get(f'step-{step_index}-description'),
                    'due_date': request.POST.get(f'step-{step_index}-due_date'),
                    'completed': False
                })
        task_data = {
            'name': task_name,
            'description': task_description,
            'due_date': task_due_date,
            'resources': task_resources,
            'tags': task_tags,
            'steps': steps
        }
        
        print("Sending Task Data to Data Endpoint:", task_data)
        response = requests.post(f"{BASE_API_URL}/create/", json=task_data)
        if response.status_code == 200:
            return redirect('listtasks')
        else:
            return JsonResponse({'error': 'Failed to create task'}, status=400)
    return render(request,'create.html')
