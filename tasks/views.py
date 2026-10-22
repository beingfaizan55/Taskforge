from rest_framework import viewsets
from rest_framework_api_key.permissions import HasAPIKey
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .permissions import IsAdminRole, IsManagerRole, IsOwnerOrCollaborator

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [HasAPIKey & (IsAdminRole | IsManagerRole | IsOwnerOrCollaborator)]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [HasAPIKey & (IsAdminRole | IsManagerRole | IsOwnerOrCollaborator)]