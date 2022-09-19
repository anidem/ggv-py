# settings/dev.py
# django v1.10

from .base import *

# Stored in environment variable -- not here.
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ggvdbruby',
        'USER': 'postgres',
        'PASSWORD': '1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Allow all host headers
ALLOWED_HOSTS = ['*']

# INSTALLED_APPS += (
# 'debug_toolbar', # This breaks the pres player -- conflicts with prototype.
# )

# USE CONSOLE EMAIL BACKEND TO PREVENT EMAILS FROM BEING SENT.
# COMMENT LINE TO ALLOW DEVS TO SEND REAL EMAILS.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587

# STATIC_ROOT = '/Library/WebServer/Documents/static'
# STATIC_URL = 'http://ggv2.developers.com/static/'

MEDIA_ROOT = '/Library/WebServer/Documents/ggv/media'
MEDIA_URL = 'http://localhost/ggv/media/'

STACKS_ROOT = '/Library/WebServer/Documents/ggv/stacks'
STACKS_URL = 'http://localhost/ggv/stacks/'
STACKS_DATA_DIR = 'data'

ARCHIVE_DATA_DIR = '/Users/rmedina/pythonweb/archives'

PDF_ROOT = '/Library/WebServer/Documents/media/pdf'

# sendfile.backends.xsendfile
SENDFILE_BACKEND = 'sendfile.backends.development'

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ[
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ[
    'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']  # This is the Client ID (not a key)

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', 'username', 'id', 'first_name', 'last_name',]
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = []
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
FIELDS_STORED_IN_SESSION = ['hash', ]

SOCIAL_AUTH_LOGIN_ERROR_URL = '/access-forbidden/'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',

    'core.utils.ggv_auth_allowed',
    'core.utils.ggv_social_user',

    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

# LOGIN_URL = '/login/google-oauth2/'
LOGIN_REDIRECT_URL = '/home'
LOGOUT_URL = '/logout/'

SESSION_SECURITY_INSECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SECURITY_WARN_AFTER =  5000 # 5 mins to move mouse
SESSION_SECURITY_EXPIRE_AFTER = 5001 # expire after 30 mins

GRADER_ID = 1

BOOTSTRAP_PREFIX = 'http://localhost/bootstrap-3.2.0'

