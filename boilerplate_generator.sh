#!/bin/bash

# --- CONFIGURATION VARIABLES ---
PROJECT_NAME="uat_tool"
DJANGO_APP="uat"
VUE_APP="uat-frontend"
VENV_NAME="venv"

# --- SET UP DJANGO BACKEND ---
echo "🔥 Setting up Django backend..."

# Create virtual environment
python3 -m venv $VENV_NAME
source $VENV_NAME/bin/activate

# Install Django and DRF
pip install django djangorestframework

# Start Django project and app
django-admin startproject $PROJECT_NAME
cd $PROJECT_NAME
python manage.py startapp $DJANGO_APP

# Generate Django models
echo "✨ Creating Django models..."
cat <<EOF > $DJANGO_APP/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

class CustomUser(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('tester', 'Tester'), ('viewer', 'Viewer')])

class System(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="systems")
    description = models.TextField(blank=True, null=True)

class Functionality(models.Model):
    name = models.CharField(max_length=255)
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="functionalities")
    description = models.TextField(blank=True, null=True)

class TestCase(models.Model):
    functionality = models.ForeignKey(Functionality, on_delete=models.CASCADE, related_name="test_cases")
    title = models.CharField(max_length=255)
    description = models.TextField()
    expected_result = models.TextField()

class TestStep(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name="steps")
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    expected_result = models.TextField()

EOF

# Generate serializers
echo "🚀 Creating Django serializers..."
cat <<EOF > $DJANGO_APP/serializers.py
from rest_framework import serializers
from .models import Organization, CustomUser, System, Functionality, TestCase, TestStep

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = '__all__'

class FunctionalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Functionality
        fields = '__all__'

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'

class TestStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStep
        fields = '__all__'

EOF

# Generate views
echo "🛠️ Creating Django views..."
cat <<EOF > $DJANGO_APP/views.py
from rest_framework import viewsets
from .models import Organization, System, Functionality, TestCase, TestStep
from .serializers import OrganizationSerializer, SystemSerializer, FunctionalitySerializer, TestCaseSerializer, TestStepSerializer

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

EOF

# Generate URLs
echo "🔗 Setting up Django URLs..."
cat <<EOF > $DJANGO_APP/urls.py
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

EOF

# Migrate models
python manage.py makemigrations $DJANGO_APP
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# --- SET UP VUE 3 FRONTEND ---
echo "🌟 Setting up Vue 3 frontend..."

# Install Vue 3 with Vite
cd ..
npm create vite@latest $VUE_APP -- --template vue
cd $VUE_APP
npm install axios

# Generate screens
echo "✨ Creating Vue screens..."
mkdir -p src/views src/components

# Home Dashboard
cat <<EOF > src/views/HomeView.vue
<template>
  <h1>Welcome to UAT Test Tool</h1>
</template>

<script setup>
</script>
EOF

# Systems Screen
cat <<EOF > src/views/SystemsView.vue
<template>
  <h1>Systems</h1>
</template>

<script setup>
</script>
EOF

# Test Cases Screen
cat <<EOF > src/views/TestCasesView.vue
<template>
  <h1>Test Cases</h1>
</template>

<script setup>
</script>
EOF

# Defects Screen
cat <<EOF > src/views/DefectsView.vue
<template>
  <h1>Defects</h1>
</template>

<script setup>
</script>
EOF

# Set up Vue Router
cat <<EOF > src/router.js
import { createRouter, createWebHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";
import SystemsView from "./views/SystemsView.vue";
import TestCasesView from "./views/TestCasesView.vue";
import DefectsView from "./views/DefectsView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/systems", component: SystemsView },
  { path: "/testcases", component: TestCasesView },
  { path: "/defects", component: DefectsView }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
EOF

# Finish setup
echo "🎉 UAT Tool setup complete!"
echo "🚀 Backend running at http://localhost:8005/"
echo "🌟 Frontend running at http://localhost:5173/"

