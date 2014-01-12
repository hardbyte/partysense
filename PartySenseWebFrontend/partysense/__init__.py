import urllib
import logging
import json
logger = logging.getLogger(__name__)


def fb_request(request, fields):

    logger.warning("Making facebook request")
    fb_user_id = request.user.social_auth.get().uid
    token = request.user.social_auth.get().tokens
    return fb_api(fb_user_id, token, fields)


def fb_api(uid, token, fields):
    fb_api = 'https://graph.facebook.com/'

    try:
        res = json.load(urllib.urlopen(fb_api + uid + "?" + urllib.urlencode({
            "access_token": token,
            "fields": fields
        })))
    except Exception as e:
        logger.warning("Something went wrong in facebook query...")
        logger.warning(e)
        res = {}
    return res