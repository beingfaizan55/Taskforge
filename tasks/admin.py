from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Project, Task

# CustomUser mein role field dikhane ke liye CustomAdmin
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ('title', 'assigned_to', 'status', 'priority', 'due_date')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'member_count', 'task_count', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'description', 'owner__username')
    filter_horizontal = ('members',)
    inlines = [TaskInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('owner').prefetch_related('members', 'tasks')

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'

    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Tasks'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project', 'assigned_to', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'project', 'due_date')
    search_fields = ('title', 'description', 'project__name', 'assigned_to__username')
    list_editable = ('status', 'priority')
    filter_horizontal = ('collaborators',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('project', 'assigned_to').prefetch_related('collaborators')