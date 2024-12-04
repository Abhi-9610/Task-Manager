from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return self.username
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks_assigned')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks_received')
    deadline = models.DateField()
    assigned_date = models.DateField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    feedback = models.TextField(blank=True, null=True)
    task_description = models.TextField()
    PROGRESS_CHOICES = [
        ('nothing', ' Nothing'),
        ('not_started', 'Not Started'),
        ('started', 'Started'),
        ('in_between', 'In Between'),
        ('completed', 'Completed'),
    ]

    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='nothing')  # 0 to 100 to indicate progress

    def __str__(self):
        return f"Task '{self.task_description[:20]}...' assigned to {self.assigned_to.username}"