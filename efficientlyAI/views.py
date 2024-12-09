from django.shortcuts import render
from rest_framework.views import Response,APIView,status
from requests import get,post
import json
from .ai import *
# Create your views here.

root = f""

def get_base_path(request):
    global root
    if root == "":
        root = f"http://{request.get_host()}"
        return
    
def check_user(userId):
    if not userId:
        return Response({"message":"userId not found"})
    headers = {'userId':userId}
    response = get(f"{root}/data/v2/getapi/",headers=headers)
    return response

class taskCreateView(APIView):
    def post(self,request):
        get_base_path(request)
        print("Reached here !!!")
        userId = request.headers.get('userId')
        response = check_user(userId=userId)
        print("Reached here !!!")
        if response.status_code==200:
            api_key = response.json()['key']
        else:
            return response
        try:
            response = generate(user_request=json.loads(request.body)['user_request'],api_key=api_key)
        except Exception as e:
            return Response({"Error":str(Exception)},status=status.HTTP_400_BAD_REQUEST)
        return Response(response,status = status.HTTP_200_OK)
    