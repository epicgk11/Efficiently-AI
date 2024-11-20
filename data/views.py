from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import *
import json
from .encryption_helper import encrypt_user_id,decrypt_user_id
@csrf_exempt
def registerUserView(request):
    if request.method == 'POST':
        id = request.headers.get('Encrypted-ID')
        existing_user = usersCollection.find_one({'Encrypted-ID':id})
        if existing_user:
            return JsonResponse({'message': 'User already exists'}, status=400)
        user_data = {
            "Encrypted-ID":id
        }
        createUser(user_data)
        return JsonResponse({'message': 'User registered successfully'})

@csrf_exempt
def createTaskView(request):
    if request.method == 'POST':
        encrypted_id = request.headers.get('Encrypted-ID')
        if not encrypted_id:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        task_data = json.loads(request.body)
        created_task = addTaskToUser(encrypted_id, task_data)
        return JsonResponse({'message': 'Task created successfully', 'task': created_task})

@csrf_exempt
def updateTaskView(request, task_id):
    if request.method == 'POST':
        encrypted_id = request.headers.get('Encrypted-ID')
        if not encrypted_id:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        task_updates = json.loads(request.body)
        updateUserTask(encrypted_id, task_id, task_updates)
        return JsonResponse({'message': 'Task updated successfully'})

@csrf_exempt
def deleteTaskView(request, task_id):
    if request.method == 'DELETE':
        encrypted_id = request.headers.get('Encrypted-ID')
        if not encrypted_id:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        deleteUserTask(encrypted_id, task_id)
        return JsonResponse({'message': 'Task deleted successfully'})

@csrf_exempt
def listTasksView(request):
    if request.method == 'GET':
        encrypted_id = request.headers.get('Encrypted-ID')
        if not encrypted_id:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        tasks = getUserTasks(encrypted_id)
        return JsonResponse({'tasks': tasks})
 