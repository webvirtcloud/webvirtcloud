"""
Django production settings for WebVirtCloud project.

"""
from .base import *

# Django settings
DEBUG = False
ADMIN_ENABLED = True

try:
    from .local import *
except ImportError:
    pass
