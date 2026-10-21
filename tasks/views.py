from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

# 1. The Frontend Dashboard View (This fixes your error!)
def dashboard_view(request):
    return render(request, 'tasks/dashboard.html')

# 2. The Custom APIView
class CapstoneHealthAPIView(APIView):
    """A basic APIView for a custom endpoint that doesn't fit standard CRUD."""
    def get(self, request):
        return Response({
            "status": "healthy",
            "message": "DRF APIView is fully operational!"
        })

# 3. The Automated ViewSets
class ProjectViewSet(viewsets.ModelViewSet):
    """Automatically handles GET, POST, PUT, PATCH, and DELETE for Projects."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """Automatically handles GET, POST, PUT, PATCH, and DELETE for Tasks."""
    queryset = Task.objects.select_related('project', 'assigned_to').prefetch_related('collaborators').all()
    serializer_class = TaskSerializer