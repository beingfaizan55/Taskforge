from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied

# 4 Tables Import kar lein
from .models import Workspace, Project, Task, TaskComment
from .serializers import WorkspaceSerializer, ProjectSerializer, TaskSerializer, TaskCommentSerializer
from .permissions import IsOwnerOrCollaborator
from .exceptions import TaskLimitExceeded

# 1. WORKSPACE VIEWSET (Top Level)
class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsOwnerOrCollaborator]
    permission_classes = [IsAuthenticated, IsOwnerOrCollaborator]
    def get_queryset(self):
        # Sirf apne Workspaces dekhain
        return Workspace.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        # Owner ID manual assign hogi
        serializer.save(owner_id=self.request.user.id)


# 2. PROJECT VIEWSET
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrCollaborator] 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        return Project.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        workspace_id = serializer.validated_data.get('workspace_id')
        
        # SECURITY CHECK 1: Kya yeh workspace is user ka hai?
        if not Workspace.objects.filter(id=workspace_id, owner_id=self.request.user.id).exists():
            raise PermissionDenied("Aap sirf apne Workspace mein project bana sakte hain.")
            
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
        # APPLICATION-LEVEL JOIN: Apne projects nikal kar unke tasks filter karein
        user_project_ids = Project.objects.filter(
            owner_id=self.request.user.id
        ).values_list('id', flat=True)
        
        return Task.objects.filter(project_id__in=user_project_ids)

    def perform_create(self, serializer):
        project_id = serializer.validated_data.get('project_id')
        
        # SECURITY CHECK 2: Kya yeh project is user ka hai?
        if not Project.objects.filter(id=project_id, owner_id=self.request.user.id).exists():
            raise PermissionDenied("Aap sirf apne projects mein hi task add kar sakte hain.")

        # LIMIT CHECK
        if Task.objects.filter(project_id=project_id).count() >= 10:
            raise TaskLimitExceeded()
            
        serializer.save()


# 4. TASK COMMENT VIEWSET (New)
class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsOwnerOrCollaborator]

    def get_queryset(self):
        # DOUBLE JOIN: Pehle mere projects, phir unke tasks, phir un tasks ke comments
        my_project_ids = Project.objects.filter(owner_id=self.request.user.id).values_list('id', flat=True)
        my_task_ids = Task.objects.filter(project_id__in=my_project_ids).values_list('id', flat=True)
        
        return TaskComment.objects.filter(task_id__in=my_task_ids)

    def perform_create(self, serializer):
        task_id = serializer.validated_data.get('task_id')
        
        # SECURITY CHECK 3: Kya jis task par comment ho raha hai, wo is user ke project ka hai?
        my_project_ids = Project.objects.filter(owner_id=self.request.user.id).values_list('id', flat=True)
        if not Task.objects.filter(id=task_id, project_id__in=my_project_ids).exists():
            raise PermissionDenied("Aap sirf apne tasks par comment kar sakte hain.")
            
        # user_id manual assign hogi (kyunke FK nahi hai)
        serializer.save(user_id=self.request.user.id)