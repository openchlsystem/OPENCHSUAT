from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.exceptions import ValidationError
import pyotp
import uuid






# User & Organization
class Organization(models.Model):
    """
    Represents an organization in the system.
    """
    name = models.CharField(max_length=255, unique=True, help_text="The name of the organization.")
    description = models.TextField(blank=True, null=True, help_text="A brief description of the organization.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the organization was created.")

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    """
    Custom user manager for the User model.
    """
    def create_user(self, whatsapp_number, password=None, **extra_fields):
        if not whatsapp_number:
            raise ValueError("The WhatsApp number field must be set")
        user = self.model(whatsapp_number=whatsapp_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, whatsapp_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(whatsapp_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # Define role choices as a class-level attribute
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('tester', 'Tester'),
        ('viewer', 'Viewer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    whatsapp_number = models.CharField(max_length=15, unique=True, help_text="The user's WhatsApp number.")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users', null=True, help_text="The organization the user belongs to.")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin', help_text="The role of the user.")
    otp_secret = models.CharField(max_length=255, blank=True, null=True, help_text="The OTP secret for two-factor authentication.")
    is_active = models.BooleanField(default=True, help_text="Indicates whether the user is active.")
    is_staff = models.BooleanField(default=False, help_text="Indicates whether the user is a staff member.")
    first_name = models.CharField(max_length=100, null=True, blank=True, help_text="The user's first name.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the user was created.")
    last_login = models.DateTimeField(null=True, blank=True, help_text="The date and time of the user's last login.")

    objects = UserManager()

    USERNAME_FIELD = "whatsapp_number"

    def __str__(self):
        return f"{self.whatsapp_number} ({self.role})"

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



# User organization Join Table 
class UserOrganization(models.Model):
    """
    Represents the join table between User and Organization.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_organizations', help_text="The user associated with the organization.")
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='user_organizations', help_text="The organization the user belongs to.")
    
    # Unique together
    class Meta:
        unique_together = ('user', 'organization')


# System & Functionality
class System(models.Model):
    """
    Represents a system in the organization.
    """
    name = models.CharField(max_length=255, help_text="The name of the system.")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='systems', help_text="The organization the system belongs to.")
    description = models.TextField(blank=True, null=True, help_text="A brief description of the system.")

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

class Functionality(models.Model):
    """
    Represents a functionality within a system.
    """
    name = models.CharField(max_length=255, help_text="The name of the functionality.")
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='functionalities', help_text="The system the functionality belongs to.")
    description = models.TextField(blank=True, null=True, help_text="A brief description of the functionality.")

    def __str__(self):
        return f"{self.name} ({self.system.name})"

# Test Cases
class TestCase(models.Model):
    """
    Represents a test case for a functionality.
    """
    title = models.CharField(max_length=255, help_text="The title of the test case.")
    functionality = models.ForeignKey(Functionality, on_delete=models.CASCADE, related_name='test_cases', help_text="The functionality this test case belongs to.")
    description = models.TextField(help_text="A detailed description of the test case.")
    expected_result = models.TextField(help_text="The expected result of the test case.")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, help_text="The user who created this test case.")
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_test_cases', blank=True, help_text="The user assigned to this test case.")
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('ready_for_testing', 'Ready for Testing'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='draft', help_text="The status of the test case.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the test case was created.")

    def __str__(self):
        return f"{self.title} ({self.functionality.name})"

class TestStep(models.Model):
    """
    Represents a step within a test case.
    """
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='steps', help_text="The test case this step belongs to.")
    step_number = models.PositiveIntegerField(help_text="The step number in the test case.")
    description = models.TextField(help_text="A detailed description of the step.")
    expected_result = models.TextField(help_text="The expected result of the step.")
    attachment = models.FileField(upload_to='test_step_attachments/', blank=True, null=True, help_text="An optional attachment for the step.")

    def __str__(self):
        return f"Step {self.step_number} for {self.test_case.title}"

# Test Execution & Defects
class TestExecution(models.Model):
    """
    Represents the execution of a test case.
    """
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='executions', help_text="The test case being executed.")
    tester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='executions', help_text="The user executing the test case.")
    status = models.CharField(max_length=20, choices=[
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('blocked', 'Blocked')
    ], help_text="The status of the test execution.")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the execution.")
    started_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the execution started.")
    completed_at = models.DateTimeField(blank=True, null=True, help_text="The date and time when the execution was completed.")

    def __str__(self):
        return f"Execution of {self.test_case.title} by {self.tester.whatsapp_number}"

    def clean(self):
        if self.completed_at and self.started_at and self.completed_at < self.started_at:
            raise ValidationError("Completion time cannot be before start time.")

class Defect(models.Model):
    """
    Represents a defect identified during a test execution.
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    execution = models.ForeignKey(TestExecution, on_delete=models.CASCADE, related_name='defects', help_text="The test execution during which this defect was identified.")
    title = models.CharField(max_length=255, help_text="A brief title summarizing the defect.")
    description = models.TextField(help_text="A detailed description of the defect, including steps to reproduce.")
    severity = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], help_text="The severity level of the defect.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    resolved = models.BooleanField(default=False, help_text="Indicates whether the defect has been resolved.")
    resolution_notes = models.TextField(blank=True, null=True, help_text="Notes on how the defect was resolved.")
    attachment = models.FileField(upload_to='defects_attachments/', blank=True, null=True,
     help_text="An optional attachment for the step.")
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reported_defects', help_text="The user who reported this defect.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the defect was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time when the defect was last updated.")

    def __str__(self):
        return f"Defect: {self.title} ({self.get_severity_display()})"

    def clean(self):
        if self.resolved and not self.resolution_notes:
            raise ValidationError({
                'resolution_notes': 'Resolution notes are required when marking the defect as resolved.'
            })

    class Meta:
        verbose_name = "Defect"
        verbose_name_plural = "Defects"
        ordering = ['-created_at']  # Order defects by creation date (newest first)