from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. CustomUser
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'Normal User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

# 2. Workspace (Top Level)
class Workspace(models.Model):
    name = models.CharField(max_length=255)
    owner_id = models.IntegerField(db_index=True)
    member_ids = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 3. Project
class Project(models.Model):
    title = models.CharField(max_length=255, default='Untitled')
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    workspace_id = models.IntegerField(db_index=True, null=True, blank=True) # Logical link to Workspace
    owner_id = models.IntegerField(db_index=True)
    member_ids = models.JSONField(default=list, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

# 4. Task
class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'To Do'
        IN_PROGRESS = 'In Progress'
        DONE = 'Done'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField(null=True, blank=True)

    project_id = models.IntegerField(db_index=True)
    assigned_to_id = models.IntegerField(null=True, blank=True, db_index=True)
    collaborator_ids = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.CharField(max_length=50, blank=True, null=True)
    estimated_hours = models.FloatField(blank=True, null=True)
    
    class Meta:
        ordering = ['due_date', '-created_at']

    def __str__(self):
        return f"[{self.status}] {self.title}"

# 5. TaskComment
class TaskComment(models.Model):
    text = models.TextField()
    task_id = models.IntegerField(db_index=True) 
    user_id = models.IntegerField(db_index=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on Task {self.task_id} by User {self.user_id}"