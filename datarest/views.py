from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
# Create your views here.
from .mongoUtils import MongoDB
from bson.objectid import ObjectId
mongo = MongoDB()
usersCollection = mongo.getCollection('users')
def check_databaser_server(mongo_object):
    try:
        mongo_object.client.server_info()
        return True,{"message":"Ok"}
    except Exception as e:
        return False,Response({"message":"Database temporarly down"},status=status.HTTP_404_NOT_FOUND)

database_availibility_flag,database_response = check_databaser_server(mongo)

def check_user(user_id):    
    if not database_availibility_flag:
        return database_response
    if not user_id:
        return False,Response({"message":"userId not found"},status = status.HTTP_400_BAD_REQUEST)
    existing_user = usersCollection.find_one({'userId': user_id})
    if not existing_user:
        return False,Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    return True,existing_user

class UserRegistrationView(APIView):
    def post(self,request):
        if not database_availibility_flag:
                return database_response
        user_id = request.headers.get('userId')
        existing_user = usersCollection.find_one({'userId': user_id})
        if existing_user:
            return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user_data = {
            "userId":user_id,
            "tasks":[],
            "bio":None,
            "commitments":[],
            "apiKey":None
        }
        insert_id = usersCollection.insert_one(user_data).inserted_id
        return Response({"message":"Successful","id":str(insert_id)},status = status.HTTP_201_CREATED)

class AdditionalInfoAddingGettingView(APIView):
    def post(self,request):
        if not database_availibility_flag:
                return database_response
        userId = request.headers.get('userId')
        flag,existing_user = check_user(userId)
        if not flag:
            return existing_user
        update_fields = json.loads(request.body)
        result = usersCollection.update_one(
            {'userId': userId},
            {'$set': update_fields}
        )
        return Response({'matched': result.matched_count, 'modified': result.modified_count},status=status.HTTP_200_OK)
    
    def get(self,request):
        if not database_availibility_flag:
                return database_response
        userId = request.headers.get('userId')
        flag,existing_user = check_user(userId)
        if not flag:
            return existing_user
        return_data = {
            'bio':existing_user.get('bio',None),
            'commitments':existing_user.get('commitments',[])
            }
        return Response(return_data,status = status.HTTP_200_OK)

class TaskAddView(APIView):
    def post(self,request):
        if not database_availibility_flag:
                return database_response
        userId = request.headers.get('userId')
        flag,existing_user = check_user(userId)
        if not flag:
            return existing_user
        task = json.loads(request.body)
        task['_id'] = str(ObjectId())
        result = usersCollection.update_one({'userId': userId}, {'$push': {'tasks': task}})
        return Response({'matched': result.matched_count, 'modified': result.modified_count},status = status.HTTP_200_OK)

class GetUpdateDelete(APIView):

    def put(self,request,taskId):
        if not database_availibility_flag:
                return database_response
        userId = request.headers.get('userId')
        flag,existing_user = check_user(userId)
        if not flag:
            return existing_user
        tasks = existing_user.get('tasks', [])
        updates = json.loads(request.body)
        for task in tasks:
            if task['_id'] == taskId:
                task.update(updates)
                break
        result = usersCollection.update_one({'userId': userId}, {'$set': {'tasks': tasks}})
        return Response({'matched': result.matched_count, 'modified': result.modified_count},status = status.HTTP_200_OK)

    def get(self,request,taskId):
        if not database_availibility_flag:
                return database_response
        userId = request.headers.get('userId')
        flag,existing_user = check_user(userId)
        if not flag:
            return existing_user
        for task in existing_user['tasks']:
            if task['_id'] == taskId:
                return Response({'task':task},status=status.HTTP_200_OK)
        return Response({"message":"Task Not Found"},status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,taskId):
        if not database_availibility_flag:
                return database_response
        userId = request.headers.get('userId')
        flag,existing_user = check_user(userId)
        if not flag:
            return existing_user
        tasks = [task for task in existing_user['tasks'] if task['_id'] != taskId]
        result=usersCollection.update_one({'userId': userId}, {'$set': {'tasks': tasks}})
        return Response({'matched': result.matched_count, 'modified': result.modified_count},status = status.HTTP_200_OK)

class ListTasksView(APIView):
    def get(self,request):
        if not database_availibility_flag:
                return database_response
        userId = request.headers.get('userId')
        flag,existing_user = check_user(userId)
        if not flag:
            return existing_user
        return Response({"tasks":existing_user.get('tasks', [])},status = status.HTTP_200_OK)
    

class APIKeyGetView(APIView):
     def get(self,request):
          if not database_availibility_flag:
               return database_response
          print("Reached Here !!")
          userId = request.headers.get('userId')
          flag,existing_user = check_user(userId)
          if not flag:
               return existing_user
          key = existing_user.get('apiKey')
          if not key:
               return Response({"message":"API key not set please set the same"},status=status.HTTP_400_BAD_REQUEST)
          return Response({'key':key},status=status.HTTP_200_OK)
     def post(self,request):
        userId = request.headers.get('userId')
        print(userId)
        flag,existing_user = check_user(userId)
        if not flag:
            return existing_user
        api_key = json.loads(request.body)['api_key']
        result = usersCollection.update_one(
            {'userId': userId},
            {'$set': {'apiKey':api_key}}
        )
        return Response({'matched': result.matched_count, 'modified': result.modified_count},status=status.HTTP_200_OK)
