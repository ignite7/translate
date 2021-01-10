""" Dev settings. """

# Base settings
from .base import *
from .base import env

# General
DEBUG = True
SECRET_KEY = env('DEV_SECRET_KEY')
ALLOWED_HOSTS = ['0.0.0.0']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {
            'sql_mode': env('DB_MODE')
        }
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# Apps
DEV_APPS = [
    'django_extensions'
]
INSTALLED_APPS = BASE_APPS + LOCAL_APPS + DEV_APPS

# Middleware
MIDDLEWARE = BASE_MIDDLEWARE

# Validators
AUTH_PASSWORD_VALIDATORS = BASE_AUTH_PASSWORD_VALIDATORS

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.users.models.commons.TokenBaseModel',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}
