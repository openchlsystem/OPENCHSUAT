# In uat_tool/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from uat.views import RequestOTPView, VerifyOTPView, RegisterUserView, DashboardView

urlpatterns = [
    # Change from uat/token/ to just /token/ to match axios expectations
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Change from uat/uat/ to just uat/ to eliminate the double uat
    path('uat/', include('uat.urls')),
   
    # Keep auth endpoints as they are since they're working
    path('uat/auth/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('uat/auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('uat/auth/register/', RegisterUserView.as_view(), name='register'),
   
    # Keep this for DRF browsable API if needed
    path('api-auth/', include('rest_framework.urls')),
   
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)