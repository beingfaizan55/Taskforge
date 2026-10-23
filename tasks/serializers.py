from rest_framework import serializers
from django.utils import timezone
from .models import Project, Task

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate(self, data):
        status = data.get('status')
        description = data.get('description', '')

        if status == 'completed' and not description:
            raise serializers.ValidationError({
                "description": "A description is strictly required to mark a task as completed."
            })
            
        return data