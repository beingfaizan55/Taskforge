from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .permissions import IsAdminRole, IsManagerRole, IsOwnerOrCollaborator

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # Add your custom permissions here
    permission_classes = [IsOwnerOrCollaborator] 

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    # Filter, Search and Order settings we configured earlier
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'project']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    permission_classes = [IsOwnerOrCollaborator]