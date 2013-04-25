import urllib
import urllib2
import json

def fb_request(request, fields):
    fb_api = 'https://graph.facebook.com/'
    fb_user_id = request.user.social_auth.get().uid
    res = json.load(urllib.urlopen(fb_api + fb_user_id + "?" + urllib.urlencode({
        "access_token": request.user.social_auth.get().tokens['access_token'],
        "fields": fields
    })))
    return res