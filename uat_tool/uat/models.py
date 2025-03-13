from django.db import models
from django.contrib.auth.models import AbstractUser

# User & Organization
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('tester', 'Tester'), ('viewer', 'Viewer')])
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_user_permissions",
        related_query_name="customuser",
    )

# System & Functionality
class System(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='systems')
    description = models.TextField(blank=True, null=True)

class Functionality(models.Model):
    name = models.CharField(max_length=255)
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='functionalities')
    description = models.TextField(blank=True, null=True)

# Test Cases
class TestCase(models.Model):
    title = models.CharField(max_length=255)
    functionality = models.ForeignKey(Functionality, on_delete=models.CASCADE, related_name='test_cases')
    description = models.TextField()
    expected_result = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

class TestStep(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    expected_result = models.TextField()

# Test Execution & Defects
class TestExecution(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='executions')
    tester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='executions')
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('passed', 'Passed'), ('failed', 'Failed'), ('blocked', 'Blocked')])
    notes = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)  # Added started_at
    completed_at = models.DateTimeField(blank=True, null=True)

# Added completed_at
class Defect(models.Model):
    execution = models.ForeignKey('TestExecution', on_delete=models.CASCADE, related_name='defects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')])
    resolved = models.BooleanField(default=False)
    reported_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)  # Added reported_by
    created_at = models.DateTimeField(auto_now_add=True)  # Added created_at
