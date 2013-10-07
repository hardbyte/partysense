import os, sys, site
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "partysense.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()