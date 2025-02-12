
import logging
import json
import itertools
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from amazonproduct import API, NoExactMatchesFound, TooManyRequests

from partysense.music.models import Track, IDType, ExternalID

api = API(locale="us")

logger = logging.getLogger(__name__)

try:
    amazon_type, created = IDType.objects.get_or_create(name="amazon")
except:
    print("Hopefully this is the first time you've run this...")

def chunker(iterable, n, fillvalue=None):
    """Helper function: Collect data into fixed-length chunks or blocks

    grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    """
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def search_amazon_for_track(track):
    """Searches amazon for the ASIN for a MP3 track with given name by given artist.
    Adds the external id to the given track.
    Get a dict:
    {
        'error': "Present only if stuff has gone wrong",
            OR
        'URL':   "http address of offers page",
        'price': "lowest price as a formatted string"
        'ASIN':  "The amazon id"
    }
    """
    logger.debug("Searching amazon for track: {}".format(track.pk))
    response = {}
    items = []
    try:
        items = api.item_search(
            'MP3Downloads',
            Keywords=track.artist.name,
            Title=track.name,
            ResponseGroup='Medium')
    except NoExactMatchesFound:
        logger.warning("Searched for track that amazon didn't have. pk={}".format(track.pk))
        response['error'] = "Track not found"
    except TooManyRequests:
        logger.warning("Too many amazon requests while searching for track")
        response['error'] = "Too many requests"

    for product in items:
        if not track._external_ids.filter(id_type=amazon_type).exists():
            new_external_id = track._external_ids.create(id_type=amazon_type, value=str(product.ASIN))
            #logger.info("Adding amazon ID for track {}".format(track.id))

        response['ASIN'] = str(product.ASIN)
        response['URL'] = str(product.DetailPageURL)
        if product.OfferSummary.TotalNew > 0:
            response['price'] = str(product.OfferSummary.LowestNewPrice.FormattedPrice)
        else:
            response['price'] = "(price not available)"
        logger.debug("Amazon price for track: {} = {}".format(track.pk, response['price']))
        break

    return response


def price_multiple_tracks(request):
    """
    API call for getting multiple amazon urls and prices given a list of
    tracks.
    """
    track_pks = set(json.loads(request.GET['pks']))
    asins = {}
    track_data = {}

    # We "might" have a mixture of tracks that we have amazon IDs for
    tracks = Track.objects.filter(pk__in=track_pks)
    for track in tracks:
        # First see if we have memcached the price :-)
        cache_result = cache.get("ASIN_for_pk={}".format(track.pk))
        if cache_result is not None:
            logger.info("Track price info was memcached.")
            track_data[track.pk] = cache_result
            # Note the ASIN doesn't get put in `asins` so it doesn't get queried
        elif track._external_ids.filter(id_type=amazon_type).exists():
            # Add ASIN to list to query
            try:
                aid = track._external_ids.get(id_type=amazon_type).value
            except MultipleObjectsReturned as e:
                logging.warning("Track {} has more than one amazon ID.".format(track.id))
                aid = track._external_ids.filter(id_type=amazon_type)[0].value
                for eid in track._external_ids.filter(id_type=amazon_type)[1:]:
                    eid.delete()
            asins[track.pk] = aid
        else:
            # Search and hopefully get ASIN
            response = search_amazon_for_track(track)

            # An item search will take about ~1 or ~2 seconds, so having an item
            # that doesn't exist in amazon's db quite a slow down.
            #
            # So we probably want to cache the failed search for an even longer
            # time - so that we only check if it still doesn't exist every couple
            # of days or so.
            if 'error' not in response:
                response.pop('ASIN')
                # As this is the first time we have searched for this track
                # only cache for a few hours
                cache_time = 6 * 60 * 60
            else:
                # there was an error, don't search for this for a while...
                cache_time = 48 * 60 * 60
            track_data[track.pk] = response
            cache.set("ASIN_for_pk={}".format(track.pk), response, 60 * 60 * 6)

    logger.info("Have these ASINs to lookup: {}".format(asins))

    # Look up the prices. 10 at a time

    for chunk_pks in chunker(asins.keys(), 10):
        logger.info(chunk_pks)
        chunk_asins = [str(asins[pk]) for pk in chunk_pks if pk is not None]
        logger.info(chunk_asins)
        try:
            result = api.item_lookup(*chunk_asins,  ResponseGroup='Medium')
        except TooManyRequests:
            logger.warning("Too many amazon requests")
            raise Http404("Too many requests")
        for pk, item in zip(chunk_pks, result.Items.Item):
            if item.OfferSummary.TotalNew > 0:
                price = str(item.OfferSummary.LowestNewPrice.FormattedPrice)
            else:
                price = "(price not available)"

            track_data[pk] = {"price": price, "URL": str(item.DetailPageURL)}

            cache.set("ASIN_for_pk={}".format(pk), track_data[pk], 60 * 60 * 12)

    resp = HttpResponse(content_type="application/json")
    json.dump(track_data, resp)
    return resp


def price_track(request):
    """
    API call for getting the url and price of a single track
    on Amazon

    Note: Data is cached for 12 hours
    """
    response = {}
    items = []

    track_pk = request.GET["pk"]
    logger.info("Amazon price request for track: {}".format(track_pk))

    artistname = request.GET["artist"]
    trackname = request.GET["track"]

    # look up the price in our cache
    cache_result = cache.get("ASIN_for_pk={}".format(track_pk))
    if cache_result is not None:
        response = cache_result
    else:
        track = get_object_or_404(Track, pk=track_pk)

        if not track._external_ids.filter(id_type=amazon_type).exists():
            response = search_amazon_for_track(track)
        else:
            logger.info("Already know the amazon id for this track!")
            asin = track._external_ids.get(id_type=amazon_type)

            try:
                result = api.item_lookup(asin.value,  ResponseGroup='Medium')
            except TooManyRequests:
                raise Http404("Too many requests")
            items = [result.Items.Item]
            logger.info("Received price info")
            for product in items:
                response['URL'] = str(product.DetailPageURL)
                if product.OfferSummary.TotalNew > 0:
                    response['price'] = str(product.OfferSummary.LowestNewPrice.FormattedPrice)
                else:
                    response['price'] = "(price not available)"
                break

    resp = HttpResponse(content_type="application/json")
    json.dump(response, resp)

    cache.set("ASIN_for_pk={}".format(track_pk), response, 60 * 60 * 12)
    return resp
