from django.contrib import admin
from .models import Task
from .models import UserProfile

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_description', 'due_date', 'priority', 'status', 'created_by']
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description', 'owner__username')
    def short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description

    short_description.short_description = 'Description'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']
    list_filter = ('role',)
    search_fields = ('user__username', 'role')
