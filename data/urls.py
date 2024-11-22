from django.urls import path
from .views import *

urlpatterns = [
    path('register/', registerUserView, name='register'),
    path('tasks/create/', createTaskView, name='create_task'),
    path('tasks/update/<str:task_id>/', updateTaskView, name='update_task'),
    path('tasks/delete/<str:task_id>/', deleteTaskView, name='delete_task'),
    path('tasks/', listTasksView, name='list_tasks'),
    path('tasks/<str:taskId>/',getTaskView,name='getSpeceficTask'),
    path('addinfo/',additionalInfoView,name='aditionalinfo'),
    path('getaddinfo/',getAdditionalTaskView,name='getaddinfo'),
    path('getprofilepic/',getProfilePicView,name='getprofilepic')
]
