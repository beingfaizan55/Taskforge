from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache  # 👈 IMPORTED CACHE HERE
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied

# Import all 4 Tables
from .models import Workspace, Project, Task, TaskComment
from .serializers import WorkspaceSerializer, ProjectSerializer, TaskSerializer, TaskCommentSerializer
from .permissions import IsOwnerOrCollaborator
from .exceptions import TaskLimitExceeded

# 1. WORKSPACE VIEWSET (Top Level)
class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrCollaborator]
    
    def get_queryset(self):
        # Return only the Workspaces owned by the current user
        return Workspace.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        # Manually assign the owner ID before saving
        serializer.save(owner_id=self.request.user.id)


# 2. PROJECT VIEWSET
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrCollaborator] 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        # Return only the Projects owned by the current user
        return Project.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        workspace_id = serializer.validated_data.get('workspace_id')
        
        # SECURITY CHECK 1: Does this workspace belong to the user?
        if not Workspace.objects.filter(id=workspace_id, owner_id=self.request.user.id).exists():
            raise PermissionDenied("You can only create projects in your own Workspace.")
            
        serializer.save(owner_id=self.request.user.id)


# 3. TASK VIEWSET
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrCollaborator]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'project_id'] 
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']

    def get_queryset(self):
        # APPLICATION-LEVEL JOIN: Fetch user's projects and filter tasks belonging to them
        user_project_ids = Project.objects.filter(
            owner_id=self.request.user.id
        ).values_list('id', flat=True)
        
        return Task.objects.filter(project_id__in=user_project_ids)

    # 👇 POST REQUEST (Create): Clear cache when a new task is added
    def perform_create(self, serializer):
        project_id = serializer.validated_data.get('project_id')
        
        # SECURITY CHECK 2: Does this project belong to the user?
        if not Project.objects.filter(id=project_id, owner_id=self.request.user.id).exists():
            raise PermissionDenied("You can only add tasks to your own projects.")

        # LIMIT CHECK: Maximum 10 tasks per project
        if Task.objects.filter(project_id=project_id).count() >= 10:
            raise TaskLimitExceeded()
            
        serializer.save()
        
        # CLEAR CACHE
        cache.clear()
        print("----> Cache Cleared after Create (POST)! <----")

    # 👇 PUT/PATCH REQUEST (Update): Clear cache when a task is updated
    def perform_update(self, serializer):
        serializer.save()
        
        # CLEAR CACHE
        cache.clear()
        print("----> Cache Cleared after Update (PUT/PATCH)! <----")

    # 👇 DELETE REQUEST (Destroy): Clear cache when a task is deleted
    def perform_destroy(self, instance):
        instance.delete()
        
        # CLEAR CACHE
        cache.clear()
        print("----> Cache Cleared after Delete (DELETE)! <----")

    # 👇 GET REQUEST (List): Cache for 15 minutes
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        # This will ONLY print in the terminal when data is fetched from the Database
        print("----> Fetching data from the DATABASE! <----")
        return super().list(request, *args, **kwargs)


# 4. TASK COMMENT VIEWSET (New)
class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsOwnerOrCollaborator]

    def get_queryset(self):
        # DOUBLE JOIN: First get my projects, then their tasks, then comments for those tasks
        my_project_ids = Project.objects.filter(owner_id=self.request.user.id).values_list('id', flat=True)
        my_task_ids = Task.objects.filter(project_id__in=my_project_ids).values_list('id', flat=True)
        
        return TaskComment.objects.filter(task_id__in=my_task_ids)

    def perform_create(self, serializer):
        task_id = serializer.validated_data.get('task_id')
        
        # SECURITY CHECK 3: Does the task being commented on belong to the user's project?
        my_project_ids = Project.objects.filter(owner_id=self.request.user.id).values_list('id', flat=True)
        if not Task.objects.filter(id=task_id, project_id__in=my_project_ids).exists():
            raise PermissionDenied("You can only comment on tasks within your own projects.")
            
        # Manually assign user_id
        serializer.save(user_id=self.request.user.id)