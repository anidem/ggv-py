"""
WSGI config for ggvproject project.

Note: Using dj_static to serve static files from django. See STATIC_ROOT setting
https://github.com/kennethreitz/dj-static
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ggvproject.settings.prod")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()