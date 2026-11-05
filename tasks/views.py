import os
import pickle
import __main__
from django.conf import settings

# Required imports for Google OAuth2
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache  # 👈 IMPORTED CACHE HERE

# DRF Imports
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Import all 4 Tables
from .models import Workspace, Project, Task, TaskComment
from .serializers import WorkspaceSerializer, ProjectSerializer, TaskSerializer, TaskCommentSerializer
from .permissions import IsOwnerOrCollaborator
from .exceptions import TaskLimitExceeded


# ---------------------------------------------------------
# AI MASTER MODEL CLASS & LOADER
# ---------------------------------------------------------
class TaskMasterPipeline:
    def __init__(self, vectorizer, nb_model, id3_model, linear_model):
        self.vectorizer = vectorizer
        self.nb_model = nb_model
        self.id3_model = id3_model
        self.linear_model = linear_model
        self.category_map = {'Design': 0, 'Finance': 1, 'Health': 2, 'Personal': 3, 'Study': 4, 'Work': 5}
        
    def predict_all(self, task_text):
        vec = self.vectorizer.transform([task_text])
        category = self.nb_model.predict(vec)[0]
        cat_num = self.category_map.get(category, 0)
        
        priority = self.id3_model.predict([[cat_num]])[0]
        time = self.linear_model.predict([[len(task_text), cat_num]])[0]
        
        return {
            "category": category,
            "priority": priority,
            "estimated_hours": round(max(0.5, float(time)), 1)
        }

# Trick: Tell Python this class is the same one used to create the pickle file
setattr(__main__, 'TaskMasterPipeline', TaskMasterPipeline)

# Load Master Model (Fails gracefully if file is missing)
try:
    MASTER_MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_engine', 'master_model.pkl')
    with open(MASTER_MODEL_PATH, 'rb') as f:
        master_pipeline = pickle.load(f)
except Exception as e:
    print(f"⚠️ Warning: Could not load ML model: {e}")
    master_pipeline = None


# ---------------------------------------------------------
# API VIEWSETS
# ---------------------------------------------------------

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


# 4. TASK COMMENT VIEWSET
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


# ---------------------------------------------------------
# 5. AI PREDICTION ENDPOINT
# ---------------------------------------------------------
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def predict_task_api(request):
    if not master_pipeline:
        return Response({'error': 'ML Master Model is missing or not loaded.'}, status=500)
        
    # DRF uses request.data instead of json.loads(request.body)
    task_text = request.data.get('task_text', '')
    
    if not task_text:
        return Response({'error': 'Task text is missing!'}, status=400)
        
    try:
        predictions = master_pipeline.predict_all(task_text)
        return Response({
            'success': True,
            'task_input': task_text,
            'ai_results': predictions
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)


# ---------------------------------------------------------
# 6. GOOGLE AUTH LOGIN
# ---------------------------------------------------------
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/accounts/google/login/callback/"
    client_class = OAuth2Client