import os
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(3) # Points to <repository root>

MEDIA_ROOT = PROJECT_DIR.child('media')

STATIC_URL = '/static/'

STATICFILES_DIRS = (PROJECT_DIR.child('static'), )

TEMPLATE_DIRS = PROJECT_DIR.child('templates')

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admindocs',

    'lessons',
    'questions',
    'core',
    
    'crispy_forms',

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


CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/ggv'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1

# Stored in environment variable -- not here.
SECRET_KEY = os.environ['SECRET_KEY']










