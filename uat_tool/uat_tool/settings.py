"""
Django settings for uat_tool project.

Generated by 'django-admin startproject' using Django 5.1.7.
"""

from pathlib import Path
from datetime import timedelta
import os
import os
import dj_database_url

from dotenv import load_dotenv
import os

load_dotenv()  # Load the environment variables from the .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = '/media/'  # URL prefix for media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECRET_KEY = 'django-insecure-i7m)%b6)-%^aqy+5-xlzs5y4-zl--84lr+!9(kjbw+h0@w$h76'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost','0.0.0.0']

# Application definition
INSTALLED_APPS = [
    'uat.apps.UatConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_extensions',
    'drf_spectacular',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True  # Set to False to use CORS_ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vue.js frontend running on Vite
    "http://127.0.0.1:5173",
    "http://localhost:5174",  # Vue.js frontend running on Vite
    "http://127.0.0.1:5174",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-requested-with",
]

ROOT_URLCONF = 'uat_tool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'uat_tool.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



DATABASES = {
    'default': dj_database_url.parse(
        os.getenv('DATABASE_URL'),
        conn_max_age=600,
        engine='django.db.backends.mysql'
    )
}


# Authentication
AUTH_USER_MODEL = 'uat.User'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# REST Framework
REST_FRAMEWORK = {
   'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
# ]
# # CORS
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# API Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'UAT Tool API',
    'DESCRIPTION': 'User Acceptance Testing Management System',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'