from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

class CustomUser(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('tester', 'Tester'), ('viewer', 'Viewer')])

class System(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="systems")
    description = models.TextField(blank=True, null=True)

class Functionality(models.Model):
    name = models.CharField(max_length=255)
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="functionalities")
    description = models.TextField(blank=True, null=True)

class TestCase(models.Model):
    functionality = models.ForeignKey(Functionality, on_delete=models.CASCADE, related_name="test_cases")
    title = models.CharField(max_length=255)
    description = models.TextField()
    expected_result = models.TextField()

class TestStep(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name="steps")
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    expected_result = models.TextField()

