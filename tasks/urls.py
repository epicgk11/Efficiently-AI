from django.urls import path
from .views import listTasks, createTask

urlpatterns = [
    path('', listTasks, name='listtasks'),
    path('create/', createTask, name='createtask'),
]
