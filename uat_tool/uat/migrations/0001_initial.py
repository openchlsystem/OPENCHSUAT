# Generated by Django 5.1.7 on 2025-03-28 12:41

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the organization.', max_length=255, unique=True)),
                ('description', models.TextField(blank=True, help_text='A brief description of the organization.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when the organization was created.')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('whatsapp_number', models.CharField(help_text="The user's WhatsApp number.", max_length=15, unique=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('tester', 'Tester'), ('viewer', 'Viewer')], default='admin', help_text='The role of the user.', max_length=20)),
                ('otp_secret', models.CharField(blank=True, help_text='The OTP secret for two-factor authentication.', max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Indicates whether the user is active.')),
                ('is_staff', models.BooleanField(default=False, help_text='Indicates whether the user is a staff member.')),
                ('first_name', models.CharField(blank=True, help_text="The user's first name.", max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when the user was created.')),
                ('last_login', models.DateTimeField(blank=True, help_text="The date and time of the user's last login.", null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the system.', max_length=255)),
                ('description', models.TextField(blank=True, help_text='A brief description of the system.', null=True)),
                ('organization', models.ForeignKey(help_text='The organization the system belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='systems', to='uat.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Functionality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the functionality.', max_length=255)),
                ('description', models.TextField(blank=True, help_text='A brief description of the functionality.', null=True)),
                ('system', models.ForeignKey(help_text='The system the functionality belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='functionalities', to='uat.system')),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='The title of the test case.', max_length=255)),
                ('description', models.TextField(help_text='A detailed description of the test case.')),
                ('expected_result', models.TextField(help_text='The expected result of the test case.')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('ready_for_testing', 'Ready for Testing'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='draft', help_text='The status of the test case.', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when the test case was created.')),
                ('assigned_user', models.ForeignKey(blank=True, help_text='The user assigned to this test case.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_test_cases', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(help_text='The user who created this test case.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('functionality', models.ForeignKey(blank=True, help_text='The functionality this test case belongs to.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_cases', to='uat.functionality')),
            ],
        ),
        migrations.CreateModel(
            name='TestExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('in_progress', 'In Progress'), ('passed', 'Passed'), ('failed', 'Failed'), ('blocked', 'Blocked')], help_text='The status of the test execution.', max_length=20)),
                ('notes', models.TextField(blank=True, help_text='Additional notes about the execution.', null=True)),
                ('started_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when the execution started.')),
                ('completed_at', models.DateTimeField(blank=True, help_text='The date and time when the execution was completed.', null=True)),
                ('test_case', models.ForeignKey(help_text='The test case being executed.', on_delete=django.db.models.deletion.CASCADE, related_name='executions', to='uat.testcase')),
                ('tester', models.ForeignKey(help_text='The user executing the test case.', on_delete=django.db.models.deletion.CASCADE, related_name='executions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='A brief title summarizing the defect.', max_length=255)),
                ('description', models.TextField(help_text='A detailed description of the defect, including steps to reproduce.')),
                ('severity', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], help_text='The severity level of the defect.', max_length=10)),
                ('status', models.CharField(choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('resolved', 'Resolved')], default='open', max_length=20)),
                ('resolved', models.BooleanField(default=False, help_text='Indicates whether the defect has been resolved.')),
                ('resolution_notes', models.TextField(blank=True, help_text='Notes on how the defect was resolved.', null=True)),
                ('attachment', models.FileField(blank=True, help_text='An optional attachment for the step.', null=True, upload_to='defects_attachments/')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when the defect was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='The date and time when the defect was last updated.')),
                ('reported_by', models.ForeignKey(help_text='The user who reported this defect.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reported_defects', to=settings.AUTH_USER_MODEL)),
                ('execution', models.ForeignKey(help_text='The test execution during which this defect was identified.', on_delete=django.db.models.deletion.CASCADE, related_name='defects', to='uat.testexecution')),
            ],
            options={
                'verbose_name': 'Defect',
                'verbose_name_plural': 'Defects',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TestStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.PositiveIntegerField(help_text='The step number in the test case.')),
                ('description', models.TextField(help_text='A detailed description of the step.')),
                ('expected_result', models.TextField(help_text='The expected result of the step.')),
                ('attachment', models.FileField(blank=True, help_text='An optional attachment for the step.', null=True, upload_to='test_step_attachments/')),
                ('test_case', models.ForeignKey(help_text='The test case this step belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='uat.testcase')),
            ],
        ),
        migrations.CreateModel(
            name='UserOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.ForeignKey(help_text='The organization associated with the user', on_delete=django.db.models.deletion.CASCADE, related_name='organization_users', to='uat.organization')),
                ('user', models.ForeignKey(help_text='The user associated with the organization', on_delete=django.db.models.deletion.CASCADE, related_name='user_organizations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'organization')},
            },
        ),
    ]
