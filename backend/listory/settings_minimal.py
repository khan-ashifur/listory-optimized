"""
Minimal Django settings without Celery dependencies
"""
from .settings import *

# Remove Celery configuration to avoid import errors
try:
    del CELERY_BROKER_URL
    del CELERY_RESULT_BACKEND
except:
    pass

# Disable Celery app loading
INSTALLED_APPS = [app for app in INSTALLED_APPS if 'celery' not in app.lower()]