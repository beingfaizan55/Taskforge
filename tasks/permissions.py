from rest_framework import permissions

class IsOwnerOrCollaborator(permissions.BasePermission):
    """Ensures users can only view or edit their own Projects and Tasks."""
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # If the object is a Project
        if hasattr(obj, 'owner'):
            return obj.owner == user or user in obj.members.all()
            
        # If the object is a Task
        if hasattr(obj, 'project'):
            return (
                obj.project.owner == user or
                obj.assigned_to == user or
                user in obj.collaborators.all() or
                user in obj.project.members.all()
            )
        return False

class IsAdminRole(permissions.BasePermission):
    """Custom permission to allow only users with the 'Admin' role."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Admin')

class IsManagerRole(permissions.BasePermission):
    """Custom permission to allow only users with the 'Manager' role."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Manager')