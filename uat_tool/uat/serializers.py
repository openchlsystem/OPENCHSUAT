from rest_framework import serializers
from django.db import transaction
from .models import (
    Organization, System, Functionality,
    TestCase, TestStep, TestExecution,
    Defect, User, UserOrganization
)
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class UserOrganizationSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = UserOrganization
        fields = ['id', 'user', 'organization']
        read_only_fields = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        style={'input_type': 'password'}
    )
    organizations = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        many=True,
        required=False,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'whatsapp_number', 'password', 'first_name',
            'organizations', 'role', 'is_active', 'is_staff',
            'created_at', 'last_login'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False},
            'whatsapp_number': {'validators': []}
        }

    def validate(self, data):
        whatsapp_number = data.get('whatsapp_number')
        organizations = data.get('organizations', [])

        if not whatsapp_number:
            raise serializers.ValidationError(
                {"whatsapp_number": "This field is required."}
            )

        if not organizations:
            raise serializers.ValidationError(
                {"organizations": ["At least one organization is required."]}
            )

        # Check for existing users
        existing_orgs = UserOrganization.objects.filter(
            user__whatsapp_number=whatsapp_number,
            organization__in=organizations
        ).select_related('organization').values_list('organization__name', flat=True)

        if existing_orgs and not self.instance:
            raise serializers.ValidationError({
                "whatsapp_number": f"This number is already registered in: {', '.join(existing_orgs)}"
            })

        return data

    @transaction.atomic
    def create(self, validated_data):
        organizations = validated_data.pop('organizations', [])
        password = validated_data.pop('password', None)

        # Create user first
        user = User.objects.create(**validated_data)

        if password:
            user.set_password(password)
            user.save()

        # Create UserOrganization relationships
        for org in organizations:
            UserOrganization.objects.create(user=user, organization=org)

        return user

class SystemSerializer(serializers.ModelSerializer):
   # organization = OrganizationSerializer.PrimaryKeyRelatedField(queryset=Organization.objects.all())  # ❌ Incorrect usage

    class Meta:
        model = System
        fields = ['id', 'name', 'organization', 'description']


class FunctionalitySerializer(serializers.ModelSerializer):
    #system = SystemSerializer(read_only=True)  # Serialize system as an object

    class Meta:
        model = Functionality
        fields = ['id', 'name', 'system', 'description']

# Test Step Serializer
class TestStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStep
        fields = ['id', 'test_case', 'step_number', 'description', 'expected_result', 'attachment']


class TestStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStep
        fields = [
            'id', 'test_case', 'step_number',
            'description', 'expected_result', 'attachment'
        ]
        read_only_fields = ['id']


class TestCaseSerializer(serializers.ModelSerializer):
    functionality = FunctionalitySerializer(read_only=True)
    functionality_id = serializers.PrimaryKeyRelatedField(
        queryset=Functionality.objects.all(),
        source='functionality',
        write_only=True,
        required=False,
        allow_null=True
    )
    created_by = UserSerializer(read_only=True)
    assigned_user = UserSerializer(read_only=True)
    assigned_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_user',
        write_only=True,
        required=False,
        allow_null=True
    )
    steps = TestStepSerializer(many=True, read_only=True)

    class Meta:
        model = TestCase
        fields = [
            'id', 'title', 'functionality', 'functionality_id', 'description',
            'expected_result', 'created_by', 'steps', 'assigned_user',
            'assigned_user_id', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'steps']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'expected_result': {'required': True}
        }

    def validate(self, data):
        """
        Custom validation to ensure required fields are provided
        """
        if self.context['request'].method in ['POST', 'PUT']:
            if not data.get('title'):
                raise serializers.ValidationError({"title": "This field is required."})
            if not data.get('description'):
                raise serializers.ValidationError({"description": "This field is required."})
            if not data.get('expected_result'):
                raise serializers.ValidationError({"expected_result": "This field is required."})
        return data

    def create(self, validated_data):
        """
        Handle TestCase creation with optional functionality
        """
        functionality = validated_data.pop('functionality', None)

        # Remove created_by if it exists in validated_data (it will be set by perform_create)
        validated_data.pop('created_by', None)

        test_case = TestCase.objects.create(
            functionality=functionality,
            **validated_data
        )
        return test_case

    def update(self, instance, validated_data):
        """
        Handle TestCase update with optional functionality
        """
        functionality = validated_data.pop('functionality', None)
        if functionality is not None:
            instance.functionality = functionality

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
class TestExecutionSerializer(serializers.ModelSerializer):
    test_case = serializers.PrimaryKeyRelatedField(queryset=TestCase.objects.all()) # Serialize test_case as an object
    tester = UserSerializer(read_only=True)  # Serialize tester as an object

    class Meta:
        model = TestExecution
        fields = ['id', 'test_case', 'tester', 'status', 'notes', 'started_at', 'completed_at']


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