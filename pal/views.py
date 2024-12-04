from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.role == 'admin':
        tasks = Task.objects.all()
    elif request.user.role == 'manager':
        tasks = Task.objects.filter(assigned_by=request.user)
    elif request.user.role == 'employee':
        tasks = Task.objects.filter(assigned_to=request.user)
    else:
        tasks = None
    assigned_by_filter = request.GET.get('assigned_by')
    priority_filter = request.GET.get('priority')
    deadline_filter = request.GET.get('deadline')

    if assigned_by_filter:
        tasks = tasks.filter(assigned_by__id=assigned_by_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if deadline_filter:
        tasks = tasks.filter(deadline=deadline_filter)

    # Pass available users for the filter dropdown
    users = User.objects.all()


    return render(request, 'dashboard.html', {'tasks': tasks})
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard or task list page after saving
    else:
        form = TaskForm(user=request.user)

    return render(request, 'create_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    # Retrieve the task object or show a 404 if not found
    task = get_object_or_404(Task, id=task_id)

    # Check if the current user is authorized to edit the task
    if request.user != task.assigned_by and request.user.role != 'admin':
        return redirect('dashboard')  # Redirect if the user is not authorized

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard after updating the task
    else:
        form = TaskForm(instance=task, user=request.user)

    return render(request, 'edit_task.html', {'form': form, 'task': task})