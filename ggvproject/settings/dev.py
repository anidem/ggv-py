# settings/dev.py

from .base import *

DEBUG = True

TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'localdb',
        'USER': 'djangodbuser',
        'PASSWORD': '1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Allow all host headers
ALLOWED_HOSTS = []

INSTALLED_APPS += (
    'debug_toolbar',
)