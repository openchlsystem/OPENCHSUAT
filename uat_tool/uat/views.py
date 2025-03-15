from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
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

User = get_user_model()

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class SystemViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer

class FunctionalityViewSet(viewsets.ModelViewSet):
    queryset = Functionality.objects.all()
    serializer_class = FunctionalitySerializer

class TestCaseViewSet(viewsets.ModelViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

class TestStepViewSet(viewsets.ModelViewSet):
    queryset = TestStep.objects.all()
    serializer_class = TestStepSerializer

class TestExecutionViewSet(viewsets.ModelViewSet):
    queryset = TestExecution.objects.all()
    serializer_class = TestExecutionSerializer

class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestOTPView(APIView):
    def post(self, request):
        whatsapp_number = request.data.get('whatsapp_number')
        try:
            user = User.objects.get(whatsapp_number=whatsapp_number)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        otp = user.generate_otp()
        # In a real app, send the OTP via WhatsApp using your chosen BSP
        print(f"Generated OTP for {whatsapp_number}: {otp}")

        return Response({'message': 'OTP sent.'}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    def post(self, request):
        whatsapp_number = request.data.get('whatsapp_number')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(whatsapp_number=whatsapp_number)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.verify_otp(otp):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

class StaffAuthView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)