from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Apne charon ViewSets import karein
from .views import WorkspaceViewSet, ProjectViewSet, TaskViewSet, TaskCommentViewSet

# 1. Router initialize karein (Sirf ek dafa)
router = DefaultRouter()

# 2. Apne 4 tables ke routes register karein
router.register(r'workspaces', WorkspaceViewSet, basename='workspace')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'comments', TaskCommentViewSet, basename='taskcomment')

# 3. URL Patterns
urlpatterns = [
    # SimpleJWT Login and Refresh Endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Automated CRUD URLs for 4 tables
    path('', include(router.urls)),
]