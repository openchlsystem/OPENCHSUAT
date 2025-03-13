from rest_framework import serializers
from .models import Organization, CustomUser, System, Functionality, TestCase, TestStep, TestExecution, Defect

# Organization Serializer
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'created_at']

# User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())  # Allow organization ID to be passed

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'organization', 'role', 'password']  # Include password for user creation
        extra_kwargs = {'password': {'write_only': True}} # Make password write only.

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

# System Serializer
class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ['id', 'name', 'organization', 'description']

# Functionality Serializer
class FunctionalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Functionality
        fields = ['id', 'name', 'system', 'description']

# Test Step Serializer
class TestStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStep
        fields = ['id', 'test_case', 'step_number', 'description', 'expected_result']

# Test Case Serializer
class TestCaseSerializer(serializers.ModelSerializer):
    steps = TestStepSerializer(many=True, read_only=True)

    class Meta:
        model = TestCase
        fields = ['id', 'title', 'functionality', 'description', 'expected_result', 'created_by', 'steps']

# Test Execution Serializer
class TestExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestExecution
        fields = '__all__'

# Defect Serializer
class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defect
        fields = '__all__'