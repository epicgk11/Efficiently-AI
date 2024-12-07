from django.urls import path
from .views import *
urlpatterns = [
    path("generateTask",taskCreateView.as_view,name='ai generate task')
]