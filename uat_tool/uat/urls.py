from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    OrganizationViewSet, SystemViewSet,
    FunctionalityViewSet, TestCaseViewSet, TestStepViewSet,
    TestExecutionViewSet, DefectViewSet, RegisterUserView,
    RequestOTPView, VerifyOTPView, StaffAuthView,
    UserViewSet, DashboardView, RolesView, StatusChoicesView,
    DefectOptionsView  # Add the new view here
)

# Initialize the DefaultRouter
router = DefaultRouter()

# Register viewsets with the router
router.register(r'organizations', OrganizationViewSet)
router.register(r'systems', SystemViewSet)
router.register(r'functionalities', FunctionalityViewSet)
router.register(r'test-cases', TestCaseViewSet)
router.register(r'test-steps', TestStepViewSet)
router.register(r'test-executions', TestExecutionViewSet)
router.register(r'defects', DefectViewSet)
router.register(r'users', UserViewSet)

# Define URL patterns
urlpatterns = [
    # Include router URLs under 'api/'
    path('uat/', include(router.urls)),

    # Choices endpoints
    path('uat/status-choices/', StatusChoicesView.as_view(), name='status-choices'),
    path('uat/defect-options/', DefectOptionsView.as_view(), name='defect-options'),  # New endpoint
    path('uat/roles/', RolesView.as_view(), name='roles'),

    # Authentication endpoints
    path('uat/auth/register/', RegisterUserView.as_view(), name='register'),
    path('uat/auth/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('uat/auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('uat/auth/staff-token/', StaffAuthView.as_view(), name='staff-token'),

    # JWT token endpoints
    path('uat/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('uat/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API documentation endpoints
    path('uat/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('uat/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Dashboard endpoint
    path('uat/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('uat/executions/', TestExecutionViewSet.as_view({'get': 'executions'}), name='executions-list'),
]