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
from lib import get_lines, get_form, get_json
import csv
from datetime import datetime

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
        #self.render_template('home.html', **template)
        self.render_template('index.html', **template)

class AboutHandler(BaseHandler):
    def get(self):
        template = {}
        #self.render_template('home.html', **template)
        self.render_template('about.html', **template)

class AdminHandler(BaseHandler):
    def get(self):
        template = {}
        self.render_template('admin.html', **template)

class BrowseDataModel(BaseHandler):
    def get(self):
        kinds = ["Club", "User", "Tag", "TrendingClubs"]
        models = []
        for kind in kinds:
            models.append("<hr/><h3>" + kind + "</h3>" + "<br/>".join(get_lines(kind)))

        self.response.write('<br/>'.join(models))


class EditClubHandler(BaseHandler):
    def get(self):
        pass


class JsonHandler(BaseHandler):
    def get(self, kind):
        self.response.write(get_json(kind))

class ImportClubsHandler(BaseHandler):
    def get(self):
        template = {}
        self.render_template('import-clubs.html', **template)

    def post(self):
        dr = csv.DictReader(self.request.POST.get('myfile').file)
        expected_keys = set(['Web', 'Tags', 'Name of Club',
                             'Description', 'City', 'Number', 'Survey Completed',
                             'Phone', 'Contact', 'Address', 'Latitude', 'Response',
                             'Longitude'])
        dr = list(dr)
        d0 = dr[0]
        for key_ in d0:
            if key_ not in expected_keys:
                return self.redirect("/error/unexpected_key_{0}".format(key_))
        for key_ in expected_keys:
            if key_ not in d0:
                return self.redirect("/error/missing_key_{0}".format(key_))
        dr = [d for d in dr if d['Name of Club']]
        for d in dr:
            for k in d:
                d[k] = d[k].strip()
        club_keys = [ndb.Key('Club', d['Name of Club']) for d in dr]
        clubs = ndb.get_multi(club_keys)

        clubs_to_save = []
        def same(a, b):
            return a is b or a == b


        for d, club in zip(dr, clubs):


            tags = d['Tags'].split(",")
            tags = [t.strip() for t in tags]
            if not club:
                club = Club(key=ndb.Key('Club', d['Name of Club']))
            props = ['name', 'website', 'tags', 'city', 'description', 'address', 'phone_number', 'longitude', 'latitude']
            olds = [getattr(club, prop, None) for prop in props]
            club.populate(
                name=d['Name of Club'],
                website=d['Web'],
                tags=tags,
                city=d['City']
            )
            club.description = d['Description']
            club.address = d['Address']
            club.phone_number = d['Phone']
            #ignore d['Response']
            #ignore d['Survey Completed']
            #ignore d['Contact']
            try:
                if d['Latitude']:
                    club.latitude = float(d['Latitude'])
                if d['Longitude']:
                    club.longitude = float(d['Longitude'])
            except:
                return self.redirect('/error/long-lat-{0}'.format(club.name))



            for i, j in zip(olds, [getattr(club, prop, None) for prop in props]):
                if i!=j:
                    try:
                        mis_match = unicode(j, 'utf-8') != i
                    except TypeError:
                        mis_match = True
                    if mis_match:
                        clubs_to_save.append(club)
                        break
        if not clubs_to_save:
            return self.redirect('/error/data-the-same-as-last-time-no-new-data')
        ndb.put_multi(clubs_to_save)
        self.response.write("success, updated {0} clubs".format(len(clubs_to_save)))

class ClubsJsonHandler(BaseHandler):
    def get(self):
        clubs = Club.query().fetch()
        json_dicts = []
        props = ['name', 'website', 'tags', 'city', 'description', 'address', 'phone_number', 'longitude', 'latitude']
        for club in clubs:
            d = {}
            for p in props:
                if hasattr(club, p):
                    val = getattr(club, p)
                    if val:
                        d[p] = str(val) if p in ('longitude', 'latitude') else val
            assert d
            json_dicts.append(d)
        self.response.write(json.dumps(json_dicts, sort_keys=True,indent=4))

class ClubsDeltaJsonHandler(BaseHandler):
    def get(self, year, month, day):
        try:
            year, month, day = int(year), int(month), int(day)
            last_refresh_date = datetime(year, month, day)
        except ValueError:
            return self.redirect('/error/invalid-date-year-{year}-month-{month}-day-{day}'.format(year=year, month=month, day=day))
        clubs = Club.query(Club.time_updated >= last_refresh_date).fetch()
        json_dicts = []
        props = ['name', 'website', 'tags', 'city', 'description', 'address', 'phone_number', 'longitude', 'latitude']
        for club in clubs:
            d = {}
            for p in props:
                if hasattr(club, p):
                    val = getattr(club, p)
                    if val:
                        d[p] = str(val) if p in ('longitude', 'latitude') else val
            assert d
            json_dicts.append(d)
        self.response.write(json.dumps(json_dicts, sort_keys=True,indent=4))

_routes = [
    RedirectRoute('/', HomeHandler, name="home", strict_slash=True),
    RedirectRoute('/about', AboutHandler, name="about", strict_slash=True),
    RedirectRoute('/error/<message>/', ErrorHandler, name="error", strict_slash=True),
    RedirectRoute('/admin', AdminHandler, name="admin", strict_slash=True),
    RedirectRoute('/api/all/<kind>', JsonHandler, name="json", strict_slash=True),
    RedirectRoute('/admin/browse-data-model', BrowseDataModel, name="browse-data-model", strict_slash=True),
    #RedirectRoute('/admin/edit-kind/<kind>', EditKindHandler, name="edit-kind", strict_slash=True)
    RedirectRoute('/admin/import-clubs', ImportClubsHandler, name='import-clubs', strict_slash=True),
    RedirectRoute('/api/clubs-dump', ClubsJsonHandler, name='clubs-dump', strict_slash=True),
    RedirectRoute('/api/clubs-delta/year/<year>/month/<month>/day/<day>', ClubsDeltaJsonHandler, name='clubs-dump', strict_slash=True)
]
app = webapp2.WSGIApplication(_routes, debug=True)


#class EditKindHandler(BaseHandler):
#    def get(self, kind):
#        #gives basic form to cut and paste.
#        template = {'form': get_form(kind)}
#        self.render_template('edit-kind.html', **template)
