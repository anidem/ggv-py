# settings/prod.py - configured for Heroku deployment

# april-22-2014
# To run this settings file with heroku command: foreman start, 
# the forman needs to access an environment variable as follows: (dbuser:pwd@host/dbname)

# export DATABASE_URL=postgres://djangodbuser:1@localhost/ggvdb2    

# This matches the local development database (see requirements/dev.txt). On Heroku, this is automagically set  (see your app settings)

from .base import *
import dj_database_url

DEBUG = False

TEMPLATE_DEBUG = False

DATABASES = {}

DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
# import os
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = 'staticfiles'
# STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
