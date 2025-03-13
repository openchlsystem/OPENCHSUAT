from rest_framework import viewsets
from .models import (
    Organization, CustomUser, System, Functionality, TestCase, TestStep, TestExecution, Defect
)
from .serializers import (
    OrganizationSerializer, CustomUserSerializer, SystemSerializer,
    FunctionalitySerializer, TestCaseSerializer, TestStepSerializer,
    TestExecutionSerializer, DefectSerializer
)

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

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