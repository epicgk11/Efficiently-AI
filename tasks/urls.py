from django.urls import path
from .views import listTasks, createTask, updateTask,getTask

urlpatterns = [
    path('', listTasks, name='listtasks'),
    path('create/', createTask, name='createtask'),
    path('update/<str:task_id>/', updateTask, name='updatetask'),
    path("get/<str:taskId>/",getTask,name='getTask'),
]
