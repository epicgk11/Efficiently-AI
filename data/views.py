from django.shortcuts import render
from django.http import JsonResponse
from bson.objectid import ObjectId
from .utils import *
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def createTaskView(request):
    if request.method == "POST": 
        print("Reached Here")
        if request.headers.get("Content-Type") == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
            data['tags'] = request.POST.getlist('tags')
            steps_raw = request.POST.get('steps', '[]')
            data['steps'] = json.loads(steps_raw) if steps_raw else []
        taskId = createTask(data)
        return JsonResponse({'message': 'Task created successfully', 'task_id': str(taskId)})
    

@csrf_exempt
def updateTaskView(request, taskId):
    if request.method == "POST":
        if request.headers.get("Content-Type") == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
            data['tags'] = request.POST.getlist('tags')
            steps_raw = request.POST.get('steps', '[]')
            data['steps'] = json.loads(steps_raw) if steps_raw else []
        updateTask(ObjectId(taskId), data)
        return JsonResponse({"message": "Task Updation Successful"})

@csrf_exempt
def deleteTaskView(request, taskId):
    if request.method == 'DELETE':
        deleteTask(ObjectId(taskId))
        return JsonResponse({'message': 'Task deleted successfully'})

@csrf_exempt
def getTaskView(request, taskId):
    if request.method == 'GET':
        task = getTask(ObjectId(taskId))
        return JsonResponse({'task': task})

@csrf_exempt
def listTasksView(request):
    if request.method == 'GET':
        tasks = listTasks()
        return JsonResponse({'tasks': tasks})
