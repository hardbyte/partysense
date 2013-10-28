import urllib
import logging
import json
logger = logging.getLogger(__name__)


def fb_request(request, fields):
    fb_api = 'https://graph.facebook.com/'
    try:
        logger.warning("Making facebook request")
        fb_user_id = request.user.social_auth.get().uid
        res = json.load(urllib.urlopen(fb_api + fb_user_id + "?" + urllib.urlencode({
            "access_token": request.user.social_auth.get().tokens,
            "fields": fields
        })))
    except Exception as e:
        logger.warning("Something went wrong in facebook query...")
        logger.warning(e)
        res = {}
    return res
