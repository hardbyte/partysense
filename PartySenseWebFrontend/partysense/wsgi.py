import os, sys, site
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "partysense.settings")

site.addsitedir('/home/hardbyte/.virtualenvs/pslive/lib/python2.7/site-packages')

activate_this = os.path.expanduser("~/.virtualenvs/pslive/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

# Calculate the path based on the location of the WSGI script
project = '/home/hardbyte/webapps/partysense/partysense/PartySenseWebFrontend/partysense'
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path = ['/home/hardbyte/webapps/partysense/partysense/PartySenseWebFrontend/',
            '/home/hardbyte/webapps/partysense/partysense/PartySenseWebFrontend/partysense',
            '/home/hardbyte/webapps/partysense'] + sys.path

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()