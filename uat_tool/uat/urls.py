from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    OrganizationViewSet, SystemViewSet,
    FunctionalityViewSet, TestCaseViewSet, TestStepViewSet,
    TestExecutionViewSet, DefectViewSet, RegisterUserView,
    RequestOTPView, VerifyOTPView, StaffAuthView,
    UserViewSet
)

# Initialize the DefaultRouter
router = DefaultRouter()

# Register viewsets with the router
router.register(r'organizations', OrganizationViewSet)
router.register(r'systems', SystemViewSet)
router.register(r'functionalities', FunctionalityViewSet)
router.register(r'test-cases', TestCaseViewSet)  # Fixed typo: 'test-cases' instead of 'test-cases'
router.register(r'test-steps', TestStepViewSet)  # Fixed typo: 'test-steps' instead of 'test-steps'
router.register(r'test-executions', TestExecutionViewSet)  # Fixed typo: 'test-executions' instead of 'test-executions'
router.register(r'defects', DefectViewSet)  # Fixed typo: 'defects' instead of 'defects'
router.register(r'users', UserViewSet)

# Define URL patterns
urlpatterns = [
    # Include router URLs under 'api/'
    path('api/', include(router.urls)),  # Keep this first to avoid conflicts

    # Authentication endpoints
    path('api/auth/register/', RegisterUserView.as_view(), name='register'),
    path('api/auth/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('api/auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('api/auth/staff-token/', StaffAuthView.as_view(), name='staff-token'),

    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API documentation endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),  # Swagger UI
]