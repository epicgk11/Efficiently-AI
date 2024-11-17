from django.urls import path
from .views import createTaskView, updateTaskView, deleteTaskView, getTaskView, listTasksView

urlpatterns = [
    path('create/', createTaskView, name='createTask'),
    path('update/<str:taskId>/', updateTaskView, name='updateTask'),
    path('delete/<str:taskId>/', deleteTaskView, name='deleteTask'),
    path('get/<str:taskId>/', getTaskView, name='getTask'),
    path('list/', listTasksView, name='listTasks')
]
