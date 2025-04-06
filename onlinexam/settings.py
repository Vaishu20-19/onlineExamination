"""
Django settings for onlinexam project.
Azure-optimized production configuration
"""

import os
from pathlib import Path
import socket

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security - All sensitive values from environment
SECRET_KEY = os.environ['SECRET_KEY']  # Must be set in Azure App Settings
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Azure-specific host configuration
hostname = socket.gethostname()
ALLOWED_HOSTS = [
    'onlinexaminatoin.azurewebsites.net',
    'localhost',
    '127.0.0.1'
]
if not DEBUG:
    ALLOWED_HOSTS = [os.environ.get('WEBSITE_HOSTNAME', 'onlinexaminatoin.azurewebsites.net')]

CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS]

# Application definition (optimized for production)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'whitenoise.runserver_nostatic',  # Must come before staticfiles
    
    # Local apps
    'exam',
    'teacher',
    'student',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Immediately after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database configuration (SQLite for dev, PostgreSQL for production)
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'OPTIONS': {'sslmode': 'require'},
        }
    }

# Static files (Azure-optimized)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security headers (auto-enabled in production)
if not DEBUG:
    SECURE_HSTS_SECONDS = 2_592_000  # 30 days
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Azure-specific optimizations
if 'WEBSITE_SITE_NAME' in os.environ:
    # Cache static files in memory
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_MANIFEST_STRICT = False
    WHITENOISE_MAX_AGE = 3600  # 1 hour cache
