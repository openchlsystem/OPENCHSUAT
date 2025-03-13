from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, SystemViewSet, FunctionalityViewSet, TestCaseViewSet, TestStepViewSet

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'systems', SystemViewSet)
router.register(r'functionalities', FunctionalityViewSet)
router.register(r'testcases', TestCaseViewSet)
router.register(r'teststeps', TestStepViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

