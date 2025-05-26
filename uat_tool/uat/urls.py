# In your uat/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    OrganizationViewSet, SystemViewSet,
    FunctionalityViewSet, TestCaseViewSet, TestStepViewSet,
    TestExecutionViewSet, DefectViewSet, RegisterUserView,
    RequestOTPView, VerifyOTPView, StaffAuthView,
    UserViewSet, DashboardView, RolesView, StatusChoicesView,
    DefectOptionsView, TesterDashboardView
)

urlpatterns = [
    # API endpouuids
    path('organizations/', OrganizationViewSet.as_view({'get': 'list', 'post': 'create'}), name='organization-list'),
    path('organizations/<int:pk>/', OrganizationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='organization-detail'),
    
    path('systems/', SystemViewSet.as_view({'get': 'list', 'post': 'create'}), name='system-list'),
    path('systems/<int:pk>/', SystemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='system-detail'),
    
    path('functionalities/', FunctionalityViewSet.as_view({'get': 'list', 'post': 'create'}), name='functionality-list'),
    path('functionalities/<int:pk>/', FunctionalityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='functionality-detail'),
    
     path('test-cases/', TestCaseViewSet.as_view({'get': 'list', 'post': 'create'}), name='testcase-list'),
    path('test-cases/<int:pk>/', TestCaseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='testcase-detail'),
    # ADD THIS LINE for test case assignment
    path('test-cases/<int:pk>/assign/', TestCaseViewSet.as_view({'post': 'assign'}), name='testcase-assign'),
   
    path('test-steps/', TestStepViewSet.as_view({'get': 'list', 'post': 'create'}), name='teststep-list'),
    path('test-steps/<int:pk>/', TestStepViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='teststep-detail'),
    
    path('test-executions/', TestExecutionViewSet.as_view({'get': 'list', 'post': 'create'}), name='testexecution-list'),
    path('test-executions/<int:pk>/', TestExecutionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='testexecution-detail'),
    path('test-executions/<int:pk>/execute/', TestExecutionViewSet.as_view({'post': 'execute'}), name='testexecution-execute'),
    
    path('defects/', DefectViewSet.as_view({'get': 'list', 'post': 'create'}), name='defect-list'),
    path('defects/<uuid:pk>/', DefectViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='defect-detail'),
    
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<uuid:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),

    # Choices endpouuids
    path('status-choices/', StatusChoicesView.as_view(), name='status-choices'),
    path('defect-options/', DefectOptionsView.as_view(), name='defect-options'),
    path('roles/', RolesView.as_view(), name='roles'),
    
    # Authentication endpouuids (these might be duplicated with the project-level URLs)
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/staff-token/', StaffAuthView.as_view(), name='staff-token'),
    
    # JWT token endpouuids (might be duplicated with the project-level URLs)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Documentation endpouuids
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Dashboard endpouuids
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('tester-dashboard/', TesterDashboardView.as_view(), name='tester-dashboard'),
    path('executions/', TestExecutionViewSet.as_view({'get': 'executions'}), name='executions-list'),
]