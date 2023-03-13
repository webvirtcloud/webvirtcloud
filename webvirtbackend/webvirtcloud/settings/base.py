"""
Django settings for webvirtcloud project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-8gyd_q$%c$(g$#nwqzbgaj2*(r1x8vp_l)-d+pm1+w^w9y9$v&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = []

# Authentication definition
AUTH_USER_MODEL = "account.User"

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Project application definition
INSTALLED_APPS += [
    "api",
    "size",
    "admin",
    "image",
    "region",
    "account",
    "compute",
    "keypair",
    "project",
    "network",
    "virtance",
]

# Third party application definition
INSTALLED_APPS += [
    "crispy_forms",
    "crispy_tailwind",
    "rest_framework",
    "django_celery_results",
]

# Middleware definition
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Rest framework definition
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "webvirtcloud.views.app_exception_handler",
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PERMISSION_CLASSES": ("webvirtcloud.permissions.IsAuthenticatedAndVerified",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("webvirtcloud.authentication.TokenAuthentication",),
}

ROOT_URLCONF = "webvirtcloud.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "webvirtcloud.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "CONN_MAX_AGE": 3600,
        "NAME": os.environ.get("DB_NAME", "webvirtcloud"),
        "USER": os.environ.get("DB_USER", "root"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "root"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", 3306),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
}

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@127.0.0.1:5672")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = "django-db"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(os.path.join(BASE_DIR, ".."), 'static')]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login redirect url
LOGIN_URL = "/admin/sign_in/"
LOGIN_REDIRECT_URL = "/admin/"

# Crispy forms
CRISPY_TEMPLATE_PACK = "tailwind"
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

#
# WebVirtCloud Settings
#

# Public images URL (Distributions, Applicatons)
PUBLIC_IMAGES_URL = os.environ.get("PUBLIC_IMAGES_URL", "https://cloud-images.webvirt.cloud/")

# Compute settings
COMPUTE_PORT = os.environ.get("COMPUTE_PORT", 8884)

# Virtual machine name prefix
VM_NAME_PREFIX = os.environ.get("VM_NAME_PREFIX", "Virtance-")
