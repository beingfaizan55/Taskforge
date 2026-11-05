from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import all viewsets and the AI prediction view (Assuming app name is 'tasks')
from tasks.views import (
    WorkspaceViewSet, 
    ProjectViewSet, 
    TaskViewSet, 
    TaskCommentViewSet,
    predict_task_api,
    GoogleLogin
)

# 1. Initialize DefaultRouter for ViewSets (Handles CRUD routing automatically)
router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet, basename='workspace')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'task-comments', TaskCommentViewSet, basename='taskcomment')

# 2. Define URL Patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include all router-generated URLs (e.g., /api/tasks/)
    path('api/', include(router.urls)),
    
    # Manual path for the AI Prediction API (Since it's a Function-Based View, not a ViewSet)
    path('api/predict-task/', predict_task_api, name='predict_task_api'),
    
    # Authentication endpoint for Google Login
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),
]