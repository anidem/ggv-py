# settings/dev.py

from .base import *

DEBUG = True

TEMPLATE_DEBUG = True

# (deployment) Where <collectstatic> will put files for production.
# static_root is the absolute path to the directory where static files will be served in production.
###STATIC_ROOT = '/staticfiles/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ggvdb2',
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

# Stored in environment variable -- not here.
SECRET_KEY = os.environ['SECRET_KEY']
