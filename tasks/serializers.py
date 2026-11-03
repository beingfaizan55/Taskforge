from rest_framework import serializers
from django.utils import timezone
from .models import Workspace, Project, Task, TaskComment
from django.contrib.auth import get_user_model
from .exceptions import InvalidTaskAction

User = get_user_model()

# 1. TASK COMMENT SERIALIZER (New)
class TaskCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TaskComment
        fields = '__all__'

    def get_user_name(self, obj):
        try:
            user = User.objects.get(id=obj.user_id)
            return user.username
        except User.DoesNotExist:
            return None


# 2. TASK SERIALIZER (Updated)
class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField(read_only=True)
    assigned_to_name = serializers.SerializerMethodField(read_only=True)
    # Manual Reverse Join for Comments
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__' 

    def get_project_name(self, obj):
        try:
            project = Project.objects.get(id=obj.project_id)
            return project.title
        except Project.DoesNotExist:
            return None

    def get_assigned_to_name(self, obj):
        assigned_to_id = getattr(obj, 'assigned_to_id', None)
        if assigned_to_id:
            try:
                user = User.objects.get(id=assigned_to_id)
                return user.username
            except User.DoesNotExist:
                return None
        return None

    def get_comments(self, obj):
        comments = TaskComment.objects.filter(task_id=obj.id)
        return TaskCommentSerializer(comments, many=True).data

    def validate_due_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate(self, data):
        status = data.get('status')
        description = data.get('description', '')
        if status == 'completed' and not description:
            raise InvalidTaskAction(detail="A description is required to complete a task.")
        return data


# 3. PROJECT SERIALIZER (Updated)
class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField(read_only=True)
    owner_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__' 
        read_only_fields = ['owner_id'] 

    def get_tasks(self, obj):
        project_tasks = Task.objects.filter(project_id=obj.id)
        return TaskSerializer(project_tasks, many=True).data

    def get_owner_name(self, obj):
        try:
            user = User.objects.get(id=obj.owner_id)
            return user.username
        except User.DoesNotExist:
            return None


# 4. WORKSPACE SERIALIZER (New Top Level)
class WorkspaceSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField(read_only=True)
    owner_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Workspace
        fields = '__all__'
        read_only_fields = ['owner_id']

    def get_projects(self, obj):
        projects = Project.objects.filter(workspace_id=obj.id)
        return ProjectSerializer(projects, many=True).data

    def get_owner_name(self, obj):
        try:
            user = User.objects.get(id=obj.owner_id)
            return user.username
        except User.DoesNotExist:
            return None