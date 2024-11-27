from django.urls import path
from .views import *
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='v2 register'),
    path('additionalInfo/',AdditionalInfoAddingGettingView.as_view(),name='v2 addinfo'),
    path('tasks/create/',TaskAddView.as_view(),name='v2 createTask'),
    path('tasks/list/',ListTasksView.as_view(),name='v2 listTasks'),
    path('tasks/<str:taskId>/',GetUpdateDelete.as_view(),name='v2 getupdatedelete'),
]