from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Workspace, Project, Task, TaskComment

# 1. Custom User Admin configuration
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
admin.site.register(CustomUser, CustomUserAdmin)


# 2. Workspace Admin configuration
@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner_id', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


# 3. Project Admin configuration
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin): 
    list_display = ('id', 'title', 'owner_id', 'get_member_count', 'get_task_count', 'created_at')
    list_filter = ('created_at', 'owner_id')
    search_fields = ('title',) 

    def get_member_count(self, obj):
        # Return member count if member_ids is a valid list
        if isinstance(obj.member_ids, list):
            return len(obj.member_ids)
        return 0
    get_member_count.short_description = 'Members'

    def get_task_count(self, obj):
        # Count tasks associated with this project ID
        return Task.objects.filter(project_id=obj.id).count()
    get_task_count.short_description = 'Tasks'


# 4. Task Admin configuration with Unfold Badges and Bulk Actions
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project_id', 'assigned_to_id', 'status_badge', 'priority_badge', 'due_date')
    list_filter = ('status', 'priority', 'project_id', 'due_date')
    search_fields = ('title', 'description')
    
    # Register custom bulk actions for status updates
    actions = ['make_completed', 'make_in_progress', 'make_pending']

    def make_completed(self, request, queryset):
        updated_count = queryset.update(status='completed')
        self.message_user(request, f"{updated_count} tasks successfully marked as Completed.")
    make_completed.short_description = "Mark selected tasks as Completed"

    def make_in_progress(self, request, queryset):
        updated_count = queryset.update(status='in_progress')
        self.message_user(request, f"{updated_count} tasks successfully marked as In Progress.")
    make_in_progress.short_description = "Mark selected tasks as In Progress"

    def make_pending(self, request, queryset):
        updated_count = queryset.update(status='pending')
        self.message_user(request, f"{updated_count} tasks successfully marked as Pending.")
    make_pending.short_description = "Mark selected tasks as Pending"

    def status_badge(self, obj):
        # Map task statuses to Tailwind color classes
        colors = {
            'completed': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
            'in_progress': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
            'pending': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
        }
        css_classes = colors.get(str(obj.status).lower(), 'bg-gray-100 text-gray-800')
        display_text = obj.get_status_display() if hasattr(obj, 'get_status_display') else obj.status
        
        return format_html(
            '<span class="px-2.5 py-0.5 text-xs font-semibold rounded-full {}">{}</span>',
            css_classes,
            display_text
        )
    status_badge.short_description = 'Status'

    def priority_badge(self, obj):
        # Map task priorities to Tailwind color classes
        colors = {
            'high': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
            'medium': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
            'low': 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300',
        }
        css_classes = colors.get(str(obj.priority).lower(), 'bg-gray-100 text-gray-800')
        display_text = obj.get_priority_display() if hasattr(obj, 'get_priority_display') else obj.priority
        
        return format_html(
            '<span class="px-2.5 py-0.5 text-xs font-semibold rounded-full {}">{}</span>',
            css_classes,
            display_text
        )
    priority_badge.short_description = 'Priority'


# 5. Task Comment Admin configuration
@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_id', 'user_id', 'created_at')
    search_fields = ('text',)