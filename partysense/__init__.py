import urllib
import logging
import json
logger = logging.getLogger(__name__)


def fb_request(request, fields):

    logger.warning("Making facebook request")
    try:
        fb_social_auth = request.user.social_auth.get(provider="facebook")
    except:
        logger.warning("Couldn't find facebook user for fb_request")
        return {"error": "Sorry you need to link your facebook account"}
    fb_user_id = fb_social_auth.uid
    token = fb_social_auth.tokens
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