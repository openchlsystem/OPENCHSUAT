from rest_framework import serializers
from .models import Organization, System, Functionality, TestCase, TestStep, TestExecution, Defect, User
from django.contrib.auth import get_user_model

User = get_user_model()

# Organization Serializer
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'created_at']

# User Serializer (For your custom User model with whatsapp_number)
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())  # Use PrimaryKeyRelatedField

    class Meta:
        model = User
        fields = ('id', 'whatsapp_number', 'password', 'first_name', 'organization', 'role', 'is_active', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# System Serializer
class SystemSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)  # Serialize organization as an object

    class Meta:
        model = System
        fields = ['id', 'name', 'organization', 'description']

# Functionality Serializer
class FunctionalitySerializer(serializers.ModelSerializer):
    system = SystemSerializer(read_only=True)  # Serialize system as an object

    class Meta:
        model = Functionality
        fields = ['id', 'name', 'system', 'description']

# Test Step Serializer
class TestStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStep
        fields = ['id', 'test_case', 'step_number', 'description', 'expected_result', 'attachment']

# Test Case Serializer
class TestCaseSerializer(serializers.ModelSerializer):
    functionality = serializers.PrimaryKeyRelatedField(queryset=Functionality.objects.all())
    created_by = UserSerializer(read_only=True)  # Ensure created_by is read-only
    steps = TestStepSerializer(many=True, read_only=True)

    class Meta:
        model = TestCase
        fields = ['id', 'title', 'functionality', 'description', 'expected_result', 'created_by', 'steps', 'assigned_user', 'status', 'created_at']

        def validate(self, data):
            # Add custom validation logic if needed
            if 'functionality' not in data:
                raise serializers.ValidationError("Functionality is required.")
            return data
# Test Execution Serializer
class TestExecutionSerializer(serializers.ModelSerializer):
    test_case = serializers.PrimaryKeyRelatedField(queryset=TestCase.objects.all()) # Serialize test_case as an object
    tester = UserSerializer(read_only=True)  # Serialize tester as an object

    class Meta:
        model = TestExecution
        fields = ['id', 'test_case', 'tester', 'status', 'notes', 'started_at', 'completed_at']

# Defect Serializer
class DefectSerializer(serializers.ModelSerializer):
    execution = TestExecutionSerializer(read_only=True)
    execution_id = serializers.PrimaryKeyRelatedField(
        queryset=TestExecution.objects.all(),
        source='execution',
        write_only=True,
        required=True
    )
    reported_by = UserSerializer(read_only=True)
    reported_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reported_by',
        write_only=True,
        required=True
    )

    class Meta:
        model = Defect
        fields = [
            'id', 'title', 'description', 'severity', 'status',
            'resolved', 'resolution_notes', 'attachment',
            'execution', 'execution_id', 'reported_by', 'reported_by_id',
            'created_at', 'updated_at'
        ]