from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import pyotp
import uuid
import base64
from django.conf import settings

# User & Organization
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserManager(BaseUserManager):
    def create_user(self, whatsapp_number, password=None, **extra_fields):
        if not whatsapp_number:
            raise ValueError("The WhatsApp number field must be set")
        user = self.model(whatsapp_number=whatsapp_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, whatsapp_number, password=None):
        user = self.create_user(
            whatsapp_number=whatsapp_number,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    whatsapp_number = models.CharField(max_length=15, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users', null=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('tester', 'Tester'), ('viewer', 'Viewer')], default='tester')
    otp_secret = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "whatsapp_number"

    def generate_otp_secret(self):
        self.otp_secret = base64.b32encode(pyotp.random_base32()).decode('utf-8')
        self.save()

    def generate_otp(self):
        if not self.otp_secret:
            self.generate_otp_secret()
        return pyotp.TOTP(self.otp_secret).now()

    def verify_otp(self, otp):
        if not self.otp_secret:
            return False
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(otp)

    def get_otp_uri(self):
        if not self.otp_secret:
            self.generate_otp_secret()
        return pyotp.totp.TOTP(self.otp_secret).provisioning_uri(
            name=self.whatsapp_number, issuer_name="uat"
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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

class TestStep(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    expected_result = models.TextField()

# Test Execution & Defects
class TestExecution(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='executions')
    tester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='executions')
    status = models.CharField(max_length=20, choices=[
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('blocked', 'Blocked')
    ])
    notes = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

class Defect(models.Model):
    execution = models.ForeignKey(TestExecution, on_delete=models.CASCADE, related_name='defects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    resolved = models.BooleanField(default=False)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)