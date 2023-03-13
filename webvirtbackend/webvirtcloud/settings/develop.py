"""
Django develop settings for WebVirtCloud project.

"""
import socket

from .base import *


# Django settings
DEBUG = True
ADMIN_ENABLED = True

# Allowed hosts
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS += [
    "drf_yasg",
    "corsheaders",
    "debug_toolbar",
]

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True

# DebugToolBar
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1"]

# Middleware definition
MIDDLEWARE += [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

try:
    from .local import *
except ImportError:
    pass
