from django.urls import path
from .views import *
urlpatterns = [
    path('create/',createtask,name='createtask'),
    path('delete/<str:taskId>/',deletetask,name='deletetask'),
    path('',listtasks,name='listtasks'),
    path('update/<str:taskId>/',updatetask,name='updatetask'),
    path('register',registration,name='appregistration'),
    path('login',login_view,name='login'),
    path('logout/',logoutView,name='logout'),
    path('profile/',profile_view,name = "profileView"),
]