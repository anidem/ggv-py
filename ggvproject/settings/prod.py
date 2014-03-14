# settings/prod.py - configured for Heroku deployment

from .base import *
import dj_database_url

DEBUG = False

TEMPLATE_DEBUG = False

DATABASES = {
    'default': { }
}


DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['.herokuapp.com']

