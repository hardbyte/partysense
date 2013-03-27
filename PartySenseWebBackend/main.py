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
from lib import get_lines
import csv
from datetime import datetime
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.users import create_logout_url

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, filename, **kwargs):
        logout_url = create_logout_url("/")
        assert("logout_url" not in kwargs)
        kwargs["logout_url"] = logout_url
        self.response.write(self.jinja2.render_template(filename, **kwargs))

class ErrorHandler(BaseHandler):
    def get(self, message='unknown error'):
        template = {'message': message}
        self.render_template("error.html", **template)

class BrowseDataModel(BaseHandler):
    def get(self):
        kinds = ["Club", "User", "Tag", "TrendingClubs"]
        models = []
        for kind in kinds:
            models.append("<hr/><h3>" + kind + "</h3>" + "<br/>".join(get_lines(kind)))
        self.response.write('<br/>'.join(models))

class GetUsersJsonHandler(BaseHandler):
    def get(self):
        from lib import PEOPLE
        self.response.write(json.dumps(PEOPLE, sort_keys=True,indent=4))

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
                club.image_dict = {}
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
            d['photos'] = {}
            if hasattr(club, 'photo1'):
                d['photos'] = {
                    "photo1": club.photo1 or "",
                    "photo2": club.photo2 or "",
                    "photo3": club.photo3 or "",
                    "photo4": club.photo4 or "",
                    "photo5": club.photo5 or ""
                }
            for k in d['photos']:
                if d['photos'][k]:
                    d['photos'][k] = get_serving_url(d['photos'][k])

            json_dicts.append(d)
        self.response.write(json.dumps(json_dicts, sort_keys=True,indent=4))

class ImageManagerHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        upload_url = blobstore.create_upload_url(self.uri_for("image-upload"))
        template = {}
        clubs = Club.query()
        if not clubs:
            return self.redirect("/error/no-clubs-to-mange-image-for")
        club_names = [club.name for club in clubs]
        #club name goes to html, so must be HTML ENCODED SAFELY. HOPEFULLY OK CLUB NAMES. no checking!!
        template = {"club_names": club_names, "upload_url": upload_url}
        self.render_template("image-manager.html", **template)

class ImageUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        club_name = self.request.get('club_name', None)

        k = ndb.Key('Club', club_name)
        club = k.get()
        if club is None:
            self.redirect("/error/no-such-club")

        blob_keys = []
        count = 0
        for i in range(1, 6):
            img_i = self.get_uploads("img{0}".format(i))

            if img_i:
                blob = img_i[0]
                if blob.size > 0:
                    setattr(club, "photo{0}".format(i), blob.key())
                    count +=1
                else:
                    blob.delete()
                    self.redirect("/error/brokenohno")
        club.put()
        return self.redirect("/admin/image-upload-success/{0}".format(count))

class ImageSuccessHandler(BaseHandler):
    def get(self, num):
        self.response.write("<a href='/admin/'>home</a><br>{0} uploaded".format(num))

class TestPushNotificationHandler(BaseHandler):
    def get(self):
        data = self.send_it("APA91bGdDMjyZfJUX6sftsbUCGV9ix8_ULHsGohhksNpGLDjLYT6M0_AAXQOojMtmuO-FLgOZ9X9UMN9RuOW38JsuGeQDeTJ7eoawLNoBFycfbOIXcE_gR8B5h_3LYP-jX2W_gekiwIomzexrUnRPHYn5kY4iunkVQ")
        self.response.write(data)

    def send_it(self, regId):
        import urllib2

        json_data = {"data1":"data1", "data2":"data2", "registration_ids": [regId] }


        url = 'https://android.googleapis.com/gcm/send'
        apiKey = "AIzaSyAK_gH3DOwX-wlJMhlkX2gocxLXYboc3LM"
        myKey = "key=" + apiKey
        data = json.dumps(json_data)
        headers = {'Content-Type': 'application/json', 'Authorization': myKey}
        req = urllib2.Request(url, data, headers)
        f = urllib2.urlopen(req)
        #response = json.loads(f.read())
        #reply = {}
        #if response ['failure'] == 0:
        #    reply['error'] = '0'
        #else:
        #    response ['error'] = '1'
        #return json.dumps(reply)
        return f.read()

_routes = [
    RedirectRoute('/error/<message>/', ErrorHandler, name="error", strict_slash=True),
    RedirectRoute('/admin/browse-data-model', BrowseDataModel, name="browse-data-model", strict_slash=True),
    RedirectRoute('/admin/import-clubs', ImportClubsHandler, name='import-clubs', strict_slash=True),
    RedirectRoute('/admin/image-upload/', ImageUploadHandler, name="image-upload", strict_slash=True),
    RedirectRoute('/admin/image-upload-success/<num>', ImageSuccessHandler, name="admin", strict_slash=True),
    RedirectRoute('/admin/image-manager', ImageManagerHandler, name='image-manager', strict_slash=True),
    RedirectRoute('/api/clubs-delta/year/<year>/month/<month>/day/<day>', ClubsDeltaJsonHandler, name='clubs-dump', strict_slash=True),
    RedirectRoute('/club-manager/people', GetUsersJsonHandler, name='people', strict_slash=True),
    RedirectRoute('/test-push', TestPushNotificationHandler, name='test-push', strict_slash=True)
]


def html_handler(name):
    file_name = name + ".html"
    class HtmlHandler(BaseHandler):
        def get(self):
            template = {}
            self.render_template(file_name, **template)
    return HtmlHandler

def dumb_routes(*args):
    for name in args:
        template = "/" + name
        if template == "/index":
            template = "/"
        yield RedirectRoute(template, html_handler(name), name=name, strict_slash=True)

_routes.extend(dumb_routes("index", "about", "admin"))
app = webapp2.WSGIApplication(_routes, debug=True)
