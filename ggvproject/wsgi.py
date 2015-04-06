"""
WSGI config for ggvproject project.
"""

import os, sys
sys.path.insert(0, '/pythonweb/ggv-py/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ggvproject.settings.prod")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()