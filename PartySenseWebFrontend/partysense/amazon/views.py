

import urllib
import logging
import json
from amazonproduct import API, AWSError


api = API(locale="us")

logger = logging.getLogger(__name__)


def search(request):
    response = {}

    artist = request.GET["artist"]
    track = request.GET["track"]

    items = api.item_search('MP3Downloads', Keywords=artist,
                            Title=track, ResponseGroup='Medium')
    for product in items:
        response['ASIN'] = product.ASIN
        response['URL'] = product.DetailPageURL
        response['image'] = product.MediumImage.URL
        response['price'] = product.OfferSummary.LowestNewPrice.FormattedPrice
        break

    res = json.dumps(response)
    return res