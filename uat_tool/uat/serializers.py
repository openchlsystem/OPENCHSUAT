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
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False)

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
        fields = ['id', 'title', 'functionality', 'description', 'expected_result', 'created_by', 'steps','assigned_user']

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