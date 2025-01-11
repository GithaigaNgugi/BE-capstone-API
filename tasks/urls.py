from django.urls import path
from .views import TaskListCreateView, TaskDetailView
from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    

]
