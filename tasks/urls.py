from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CapstoneHealthAPIView, ProjectViewSet, TaskViewSet

# The Router automatically builds the URL paths for your ViewSets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    # Manually map the APIView
    path('health/', CapstoneHealthAPIView.as_view(), name='api-health'),
    
    # Automatically map all ViewSet URLs
    path('', include(router.urls)),
]