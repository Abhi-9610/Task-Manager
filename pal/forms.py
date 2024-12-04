from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.conf import settings


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

class CustomAuthenticationForm(AuthenticationForm):
    pass
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['assigned_by', 'assigned_to', 'priority', 'deadline', 'task_description', 'progress', 'feedback']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            if user.role == 'manager':
                # Managers can assign tasks to employees and other managers
                self.fields['assigned_to'].queryset = CustomUser.objects.filter(role__in=['employee', 'manager'])
            elif user.role == 'admin':
                # Admins can assign tasks to anyone
                self.fields['assigned_to'].queryset = CustomUser.objects.all()
            self.fields['assigned_by'].initial = user