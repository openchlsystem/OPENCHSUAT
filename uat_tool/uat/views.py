from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser, AllowAny
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.utils.timezone import now
from .models import (
    Organization, System, Functionality, TestCase,
    TestStep, TestExecution, Defect, User
)
from .serializers import (
    OrganizationSerializer, SystemSerializer,
    FunctionalitySerializer, TestCaseSerializer, TestStepSerializer,
    TestExecutionSerializer, DefectSerializer, UserSerializer
)
import pyotp
import requests
import random
import logging
import time

User = get_user_model()
otp_store = {}  # Temporary OTP storage with expiration

# Test Case API ViewSet
class TestCaseViewSet(viewsets.ModelViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

    @extend_schema(
        request={
            "type": "object",
            "properties": {
                "userId": {"type": "string", "description": "UUID of the user to assign"}
            },
            "required": ["userId"]
        },
        responses={
            200: {"type": "object", "properties": {"message": {"type": "string"}}},
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
        parameters=[
            OpenApiParameter(name='pk', type=OpenApiTypes.INT, description='Test case ID', location=OpenApiParameter.PATH)
        ]
    )
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        test_case = self.get_object()
        user_id = request.data.get('userId')
        if not user_id:
            return Response({'error': 'userId is required in the request body'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        test_case.assigned_user = user
        test_case.save()
        return Response({'message': 'User assigned successfully'}, status=status.HTTP_200_OK)

# Organization API ViewSet
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

# System API ViewSet
class SystemViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer

# Functionality API ViewSet
class FunctionalityViewSet(viewsets.ModelViewSet):
    queryset = Functionality.objects.all()
    serializer_class = FunctionalitySerializer

# Test Step API ViewSet
class TestStepViewSet(viewsets.ModelViewSet):
    queryset = TestStep.objects.all()
    serializer_class = TestStepSerializer

# Test Execution API ViewSet
class TestExecutionViewSet(viewsets.ModelViewSet):
    queryset = TestExecution.objects.all()
    serializer_class = TestExecutionSerializer

# Defect API ViewSet
class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer

# User API ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for user in data:
            try:
                user['organization_name'] = Organization.objects.get(id=user['organization']).name
            except Organization.DoesNotExist:
                user['organization_name'] = None

        return Response(data)

    def create(self, request, *args, **kwargs):
        data = request.data
        if data.get('created_by_admin'):
            data['role'] = 'admin'
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

# Register User API
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully!", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# OTP Request API
class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        whatsapp_number = request.data.get("whatsapp_number")
        org_id = request.data.get("org_id")  # Allow passing org_id dynamically

        if not whatsapp_number:
            return Response({"error": "WhatsApp number is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(whatsapp_number=whatsapp_number)
        except User.DoesNotExist:
            return Response({"error": "User not found. Please register first."}, status=status.HTTP_404_NOT_FOUND)

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))
        otp_store[whatsapp_number] = {"otp": otp, "expiry": time.time() + 300}  # 5 min expiry

        # Send OTP via WhatsApp API
        try:
            response = requests.post(
                "https://backend.bitz-itc.com/api/whatsapp/whatsapp/send/",
                json={
                    "recipient": whatsapp_number,
                    "message_type": "text",
                    "content": f"Your OTP is: {otp}. It expires in 5 minutes.",
                },
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)
            else:
                logging.error(f"Failed to send OTP: {response.text}")
                return Response({"error": "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.RequestException as e:
            logging.error(f"Request error while sending OTP: {e}")
            return Response({"error": "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# OTP Verification API
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        whatsapp_number = request.data.get("whatsapp_number")
        otp = request.data.get("otp")

        if not whatsapp_number or not otp:
            return Response({"error": "WhatsApp number and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        otp_data = otp_store.get(whatsapp_number)
        if otp_data and otp_data["otp"] == otp:
            if time.time() > otp_data["expiry"]:
                return Response({"error": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(whatsapp_number=whatsapp_number)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Remove OTP after successful login
            del otp_store[whatsapp_number]

            return Response({"access": access_token, "refresh": str(refresh)}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

# Staff Authentication API
class StaffAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        whatsapp_number = request.data.get("whatsapp_number")
        password = request.data.get("password")

        if not whatsapp_number or not password:
            return Response({"error": "WhatsApp number and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(whatsapp_number=whatsapp_number, is_staff=True)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials."}, status=status.HTTP_403_FORBIDDEN)

        # Generate access token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({"access": access_token}, status=status.HTTP_200_OK)