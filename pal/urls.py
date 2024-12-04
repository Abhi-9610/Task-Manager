from django.urls import path
from .views import *

urlpatterns = [
    path('', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create-task/', create_task, name='create_task'),
    path('edit-task/<int:task_id>/', edit_task, name='edit_task'),
]
