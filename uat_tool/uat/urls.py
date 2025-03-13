# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrganizationViewSet, CustomUserViewSet, SystemViewSet,
    FunctionalityViewSet, TestCaseViewSet, TestStepViewSet,
    TestExecutionViewSet, DefectViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'systems', SystemViewSet)
router.register(r'functionalities', FunctionalityViewSet)
router.register(r'test-cases', TestCaseViewSet)
router.register(r'test-steps', TestStepViewSet)
router.register(r'test-executions', TestExecutionViewSet)
router.register(r'defects', DefectViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/auth/', include('rest_framework.urls')),  # For login/logout
]