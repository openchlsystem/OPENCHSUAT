from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    OrganizationViewSet, SystemViewSet,
    FunctionalityViewSet, TestCaseViewSet, TestStepViewSet,
    TestExecutionViewSet, DefectViewSet, RegisterUserView,
    RequestOTPView, VerifyOTPView, StaffAuthView,
    UserViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'users', UserViewSet)  # Changed from CustomUserViewSet
router.register(r'systems', SystemViewSet)
router.register(r'functionalities', FunctionalityViewSet)
router.register(r'test-cases', TestCaseViewSet)
router.register(r'test-steps', TestStepViewSet)
router.register(r'test-executions', TestExecutionViewSet)
router.register(r'defects', DefectViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterUserView.as_view(), name='register'),
    path("api/auth/request-otp/", RequestOTPView.as_view(), name="request-otp"),
    path("api/auth/verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("api/auth/refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/staff-token/", StaffAuthView.as_view(), name="staff_token"),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    # path('api/auth/', include('rest_framework.urls')),  # Optional basic auth
]