# settings/heroku.py - configured for Heroku deployment
import os
from unipath import Path
import dj_database_url


PROJECT_DIR = Path(__file__).ancestor(3)  # Points to <repository root>

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)


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


MEDIA_URL = '/media/'

MEDIA_ROOT = 'media'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DIRS = PROJECT_DIR.child('templates')

# Application definition
INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admindocs',

    'courses',
    'lessons',
    'slidestacks',
    'questions',
    'core',

    'crispy_forms',
    'django_wysiwyg',
    'guardian',

    'south',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ggvproject.urls'

WSGI_APPLICATION = 'ggvproject.wsgi.application'

SITE_ID = 0

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

GRAPPELLI_ADMIN_TITLE = 'GGV Admin'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_URL = '/login'

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1

# Stored in environment variable -- not here.
SECRET_KEY = os.environ['SECRET_KEY']

