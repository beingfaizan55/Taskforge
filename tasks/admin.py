from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Workspace, Project, Task, TaskComment

# Jin models ki custom admin classes nahi hain, unhein yahan register karein
admin.site.register(Workspace)
admin.site.register(TaskComment)

# CustomUser mein role field dikhane ke liye CustomAdmin
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Project)
class ProjectAdmin(ModelAdmin := admin.ModelAdmin):
    list_display = ('id', 'title', 'owner_id', 'get_member_count', 'get_task_count', 'created_at')
    list_filter = ('created_at', 'owner_id')
    search_fields = ('title',) 

    def get_member_count(self, obj):
        # member_ids ab ek JSON list hai (jaise [1, 2, 3]), isliye len() use karenge
        if isinstance(obj.member_ids, list):
            return len(obj.member_ids)
        return 0
    get_member_count.short_description = 'Members'

    def get_task_count(self, obj):
        # Related name ('tasks') kaam nahi karega, isliye manual database query karenge
        return Task.objects.filter(project_id=obj.id).count()
    get_task_count.short_description = 'Tasks'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project_id', 'assigned_to_id', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'project_id', 'due_date')
    search_fields = ('title', 'description')
    list_editable = ('status', 'priority')