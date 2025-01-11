from rest_framework import serializers
from .models import UserProfile, Task
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role']

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    assigned_to = serializers.ReadOnlyField(source='assigned_to.username')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'created_by', 'assigned_to', 'created_at', 'updated_at']

class ClientTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
