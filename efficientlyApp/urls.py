from django.urls import path
from .views import createtask,listtasks,deletetask,updatetask,registration,login_view
urlpatterns = [
    path('create/',createtask,name='createtask'),
    path('delete/<str:taskId>/',deletetask,name='deletetask'),
    path('',listtasks,name='listtasks'),
    path('update/<str:taskId>/',updatetask,name='updatetask'),
    path('register',registration,name='appregistration'),
    path('login',login_view,name='login')
]