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
    DefectOptionsView, TesterDashboardView  # Add the new view here
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
    # Include router URLs under '/'
    path('/', include(router.urls)),

    # Choices endpoints
    path('status-choices/', StatusChoicesView.as_view(), name='status-choices'),
    path('defect-options/', DefectOptionsView.as_view(), name='defect-options'),  # New endpoint
    path('roles/', RolesView.as_view(), name='roles'),

    # Authentication endpoints
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/staff-token/', StaffAuthView.as_view(), name='staff-token'),

    # JWT token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #  documentation endpoints
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Dashboard endpoint
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('tester-dashboard/', TesterDashboardView.as_view(), name='tester-dashboard'),
    path('executions/', TestExecutionViewSet.as_view({'get': 'executions'}), name='executions-list'),
]