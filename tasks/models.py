from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class UserProfile(AbstractUser):
    """
    Custom User model with roles for manager, technician, and client.
    """
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Set unique related_name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Set unique related_name to avoid conflict
        blank=True
    )
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('technician', 'Technician'),
        ('client', 'Client'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class Task(models.Model):
    """
    Task model representing tasks in the service industry.
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(UserProfile, related_name='created_tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(UserProfile, related_name='assigned_tasks', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Custom validation to ensure due_date is greater than the current date.
        """
        if self.due_date <= now().date():
            raise ValidationError("Due date must be a future date.")

    def __str__(self):
        return self.title
