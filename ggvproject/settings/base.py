import os
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(3)  # Points to <repository root>

MEDIA_URL = '/media/'

MEDIA_ROOT = 'media'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

# heroku uses dj_static to serve static files.
# It does not require absolute path -- this is relative to development dir?


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',

    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

TEMPLATE_DIRS = [PROJECT_DIR.child('templates')]

# Application definition
INSTALLED_APPS = (
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admindocs',

    'courses',
    'lessons',
    'slidestacks',
    'questions',
    'supportmedia',
    'notes',
    'core',

    'crispy_forms',
    'django_wysiwyg',
    'guardian',
    'social.apps.django_app.default',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'ggvproject.urls'

WSGI_APPLICATION = 'ggvproject.wsgi.application'

SITE_ID = 0

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = True

GRAPPELLI_ADMIN_TITLE = 'GGV Admin'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800  # 1 day inactivity logout

GRAPPELLI_INDEX_DASHBOARD = 'ggvproject.ggvadmindashboard.CustomIndexDashboard'

FILEBROWSER_DIRECTORY = ''
FILEBROWSER_MEDIA_URL = '/media/'
FILEBROWSER_MEDIA_ROOT = 'media'

FILEBROWSER_VERSIONS_BASEDIR = '_versions'



