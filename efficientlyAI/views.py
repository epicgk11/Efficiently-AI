from django.shortcuts import render
from rest_framework.views import Response,APIView
from requests import get,post
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
    def post(request):
        userId = request.headers.get('userId')
        response = check_user(userId=userId)
        if response.status_code==200:
            api_key = response.json()['key']
        else:
            return response
        return Response({"message":api_key},status = status.HTTP_200_OK)
    