from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import *
import json


@csrf_exempt
def registerUserView(request):
    if request.method == 'POST':
        id = request.headers.get('userId')
        existing_user = usersCollection.find_one({'userId':id})
        if existing_user:
            return JsonResponse({'message': 'User already exists'}, status=400)
        user_data = {
            "userId":id
        }
        createUser(user_data)
        return JsonResponse({'message': 'User registered successfully'})


@csrf_exempt
def additionalInfoView(request):
    if request.method == 'POST':
        id = request.headers.get('userId')
        existing_user = usersCollection.find_one({'userId':id})
        if not existing_user:
            return JsonResponse({"message":"userNotFound"})
        data = json.loads(request.body)
        addAdditionalInfo(userId=id,data=data)
        return JsonResponse({"message":"Success"})

@csrf_exempt
def getAdditionalTaskView(request):
    if request.method == 'GET':
        userId = request.headers.get('userID')
        if not userId:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        tasks = getAdditionalInfo(userId)
        return JsonResponse({'additional_info': tasks})

@csrf_exempt
def getProfilePicView(request):
    if request.method=="GET":
        userId = request.headers.get('userID')
        if not userId:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        pic = getProfilePic(userId)
        return JsonResponse({'image bytes': pic})
    
@csrf_exempt
def createTaskView(request):
    if request.method == 'POST':
        userId = request.headers.get('userId')
        if not userId:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        task_data = json.loads(request.body)
        created_task = addTaskToUser(userId, task_data)
        return JsonResponse({'message': 'Task created successfully', 'task': created_task})

@csrf_exempt
def updateTaskView(request, task_id):
    if request.method == 'POST':
        userId = request.headers.get('userID')
        if not userId:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        task_updates = json.loads(request.body)
        updateUserTask(userId, task_id, task_updates)
        return JsonResponse({'message': 'Task updated successfully'})

@csrf_exempt
def deleteTaskView(request, task_id):
    if request.method == 'DELETE':
        userId = request.headers.get('userID')
        if not userId:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        deleteUserTask(userId, task_id)
        return JsonResponse({'message': 'Task deleted successfully'})

@csrf_exempt
def listTasksView(request):
    if request.method == 'GET':
        userId = request.headers.get('userID')
        if not userId:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        tasks = getUserTasks(userId)
        return JsonResponse({'tasks': tasks})
 
@csrf_exempt
def getTaskView(request,taskId):
    if request.method == "GET":
        userId = request.headers.get('userId')
        task = getSpeceficTask(userId,taskId)
        return JsonResponse(task)