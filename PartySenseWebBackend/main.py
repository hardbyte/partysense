import webapp2
from webapp2_extras import jinja2
from webapp2_extras.routes import RedirectRoute
from google.appengine.ext import ndb
from google.appengine.api.images import get_serving_url
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import cgi
import quopri
class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, filename, **kwargs):
        self.response.write(self.jinja2.render_template(filename, **kwargs))

class ErrorHandler(BaseHandler):
    def get(self, message='unknown error'):
        template = {'message': message}
        self.render_template("error.html", **template)

class HomeHandler(BaseHandler):
    def get(self):
        template = {}
        self.render_template('home.html', **template)


class AdminHandler(BaseHandler):
    def get(self):
        template = {}
        self.render_template('admin.html', **template)

class SampleJson(BaseHandler):
    def get(self):
        self.response.write('{"message": "hello world"}')

_routes = [
    RedirectRoute('/', HomeHandler, name="home", strict_slash=True),
    RedirectRoute('/error/<message>/', ErrorHandler, name="error", strict_slash=True),
    RedirectRoute('/admin', AdminHandler, name="admin", strict_slash=True),
    RedirectRoute('/api/sample-json', SampleJson, name="sample-json", strict_slash=True)
]
app = webapp2.WSGIApplication(_routes, debug=True)