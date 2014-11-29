import os, sys, site
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "partysense.settings")

# Add the site-packages of our deployment virtualenv
site.addsitedir('/home/hardbyte/.virtualenvs/pslive/lib/python2.7/site-packages')

# Add the app's directories to the python path
sys.path.append('/home/hardbyte/webapps/partysense/partysense/PartySenseWebFrontend/')
sys.path.append('/home/hardbyte/webapps/partysense/partysense/PartySenseWebFrontend/partysense')

# Activate the virtual env
activate_this = os.path.expanduser("~/.virtualenvs/pslive/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
