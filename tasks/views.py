from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task
from .serializers import TaskSerializer, ClientTaskSerializer
from .permissions import IsManager, IsTechnician, IsClient
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied



class TaskListCreateView(generics.ListCreateAPIView):
    """
    View for listing all tasks and creating a new task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the task with the current user as the creator.
        """
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks in the service industry with role-based permissions.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return different serializers based on the user's role.
        """
        if self.request.user.role == 'client':
            return ClientTaskSerializer
        return TaskSerializer

    def get_permissions(self):
        """
        Return custom permissions based on the user's role.
        """
        if self.request.user.role == 'manager':
            self.permission_classes = [IsAuthenticated, IsManager]
        elif self.request.user.role == 'technician':
            self.permission_classes = [IsAuthenticated, IsTechnician]
        elif self.request.user.role == 'client':
            self.permission_classes = [IsAuthenticated, IsClient]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Allow only managers to create tasks.
        """
        if self.request.user.role == 'manager':
            serializer.save(created_by=self.request.user)
        else:
            raise PermissionDenied("Only managers can create tasks.")

    def perform_update(self, serializer):
        """
        Allow only managers and technicians to update tasks.
        Technicians can only update 'status' and 'description'.
        """
        if self.request.user.role == 'manager':
            serializer.save()
        elif self.request.user.role == 'technician':
            allowed_fields = ['status', 'description']
            if any(field not in allowed_fields for field in serializer.validated_data):
                raise PermissionDenied("Technicians can only update the status or description.")
            serializer.save()
        else:
            raise PermissionDenied("Only managers and technicians can update tasks.")

    def perform_destroy(self, instance):
        """
        Allow only managers to delete tasks.
        """
        if self.request.user.role == 'manager':
            instance.delete()
        else:
            raise PermissionDenied("Only managers can delete tasks.")

    def list(self, request, *args, **kwargs):
        """
        Restrict fields for clients when listing tasks.
        """
        if request.user.role == 'client':
            queryset = Task.objects.all().only('title', 'description', 'status')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)

# Serializer for User registration

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # This fetches the custom User model
        fields = ('username', 'password', 'role')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        user.role = validated_data['role']
        user.save()
        return user

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return detailed validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)