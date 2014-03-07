# settings/prod.py

from .base import *
import dj_database_url

DEBUG = False

TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        # 'ENGINE':'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'localdb',
        # 'USER': 'djangodbuser',
        # 'PASSWORD': '1',
        # 'HOST': 'localhost',
        # 'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
#     }
# }

DATABASES['default'] =  dj_database_url.config() #default='postgres://djangodbuser:1@localhost/localdb'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['.herokuapp.com']

