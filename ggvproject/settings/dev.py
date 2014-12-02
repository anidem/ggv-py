# settings/dev.py

from .base import *

# Stored in environment variable -- not here.
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

TEMPLATE_DEBUG = True

# (deployment) Where <collectstatic> will put files for production.
# static_root is the absolute path to the directory where static files will be served in production.
###STATIC_ROOT = '/staticfiles/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ggvdb2',
        'USER': 'ggvdbuser',
        'PASSWORD': '1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Allow all host headers
ALLOWED_HOSTS = []

# INSTALLED_APPS += (
#     'debug_toolbar', # This breaks the pres player -- conflicts with prototype.
# )

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587

MEDIA_ROOT = '/Library/WebServer/Documents/media'
MEDIA_URL = 'http://localhost/media/'

STACKS_ROOT = '/pythonmedia/stacks'
STACKS_DATA_DIR = 'data'

SENDFILE_BACKEND = 'sendfile.backends.development'
