from django.urls import path
from .views import createtask,listtasks,deletetask,updatetask
urlpatterns = [
    path('create/',createtask,name='createtask'),
    path('delete/<str:taskId>/',deletetask,name='deletetask'),
    path('',listtasks,name='listtasks'),
    path('update/<str:taskId>/',updatetask,name='updatetask')
]