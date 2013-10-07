

import urllib
import logging
import json
from amazonproduct import API, AWSError
from django.http import HttpResponse

api = API(locale="us")

logger = logging.getLogger(__name__)


def purchase(request):
    response = {}

    artist = request.GET["artist"]
    track = request.GET["track"]

    items = api.item_search('MP3Downloads', Keywords=artist,
                            Title=track, ResponseGroup='Medium')
    for product in items:
        response['ASIN'] = str(product.ASIN)
        response['URL'] = str(product.DetailPageURL)
        response['image'] = str(product.MediumImage.URL)
        response['price'] = str(product.OfferSummary.LowestNewPrice.FormattedPrice)
        break

    resp = HttpResponse(content_type="application/json")
    json.dump(response, resp)
    return resp
