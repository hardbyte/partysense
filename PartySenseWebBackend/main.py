import webapp2
from webapp2_extras import jinja2
from webapp2_extras.routes import RedirectRoute
from google.appengine.ext import ndb
from google.appengine.api.images import get_serving_url
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import cgi
import quopri
from datamodel import Club
import json

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

class BrowseDataModel(BaseHandler):
    def get(self):
        kinds = ["Club", "User", "Tag", "TrendingClubs"]
        models = []
        for kind in kinds:
            models.append("<hr/><h3>" + kind + "</h3>" + "<br/>".join(get_lines(kind)))

        self.response.write('<br/>'.join(models))

class EditKindHandler(BaseHandler):
    def get(self, kind):
        template = {'form': get_form(kind)}
        self.render_template('edit-kind.html', **template)

class JsonHandler(BaseHandler):
    def get(self, kind):
        self.response.write(get_json(kind))

def get_lines(kind):
    end1 = "class "
    end2 = "(ndb.Model):"
    with open('datamodel.py') as f:
        lines = f.readlines()
    append = False
    chunk = []
    for line in lines:
        if append:
            if end1 in line and end2 in line:
                break
            chunk.append(line)
        if "class " + kind + "(ndb.Model):" in line:
            append = True

    return chunk

def get_form(kind):

    lines = get_lines(kind)
    form_lines = []
    form_lines.append("<form>")
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        is_string = "StringProperty" in line
        is_repeat = "repeated=True" in line
        is_int = "IntegerProperty" in line
        is_float = "FloatProperty" in line
        is_text = "TextProperty" in line
        is_key = "Key" in line
        is_date = "DateTimeProperty" in line
        assert [is_date, is_string, is_int, is_float, is_key, is_text].count(True) == 1
        if is_key or is_date:
            continue
        label = line.split("=")[0].strip()
        input_ = """<input type="text" name="{0}">""".format(label)
        if is_repeat:
            input_ = input_ * 5
        input_ += "<br/>"
        form_line = "{label}: {input_}".format(label=label, input_=input_)
        form_lines.append(form_line)
    form_lines.append("""<input type="submit" value="Submit">""")
    form_lines.append("</form>")
    return "".join(form_lines)

def get_json(kind):
    lines = get_lines(kind)
    json_dicts = []
    #print lines, 'wtf'
    for xx in "abc":
        json_dict = {}
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            is_string = "StringProperty" in line
            is_repeat = "repeated=True" in line
            is_int = "IntegerProperty" in line
            is_float = "FloatProperty" in line
            is_text = "TextProperty" in line
            is_key = "Key" in line
            is_date = "DateTimeProperty" in line
            assert [is_date, is_string, is_int, is_float, is_key, is_text].count(True) == 1
            if is_key or is_date:
                continue
            label = line.split("=")[0].strip()
            #print label
            json_dict[label] = xx
        json_dicts.append(json_dict)
    return json.dumps(json_dicts)


_routes = [
    RedirectRoute('/', HomeHandler, name="home", strict_slash=True),
    RedirectRoute('/error/<message>/', ErrorHandler, name="error", strict_slash=True),
    RedirectRoute('/admin', AdminHandler, name="admin", strict_slash=True),
    RedirectRoute('/api/sample-json', SampleJson, name="sample-json", strict_slash=True),
    RedirectRoute('/api/all/<kind>', JsonHandler, name="json", strict_slash=True),
    RedirectRoute('/admin/browse-data-model', BrowseDataModel, name="browse-data-model", strict_slash=True),
    RedirectRoute('/admin/edit-kind/<kind>', EditKindHandler, name="edit-kind", strict_slash=True)
]
app = webapp2.WSGIApplication(_routes, debug=True)