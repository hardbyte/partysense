"""

Create a ~/.amazon-product-api file with:

    [Credentials]
    access_key = AKIAJ6HNZC6HWILISCKA
    secret_key = 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
    associate_tag = 6404-2547-9415

"""

# amazon api test

from amazonproduct import API, AWSError

api = API(locale="us")

"""
195211011 - MP3Downloads browse node.
In an ItemSearch request, when the SearchIndex parameter equals "MP3Downloads",
only the following parameters can be used in the request.

* Browsenode
* Keyword
* Title

ResponseGroup = Large or Medium seems to be required to get the OfferDetails
http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_ResponseGroupsList.html
"""


items = api.item_search('MP3Downloads',
                        Keywords='Daft Punk',
                        Title='Get Lucky',
                        ResponseGroup='Medium'
                        )

for product in items:
    amazon_id = product.ASIN

    """ItemAttributes
    Creator: "Daft Punk feat.
    Genre: pop-music
    ReleaseDate: 2013-04-13
    RunningTime: 248
    Title: ""
    """
    title = product.ItemAttributes.Title


    print amazon_id, title, product.ItemAttributes.Creator
    print "URL to purchase: ", product.DetailPageURL

    # Another similar URL...?
    #print product.ItemLinks.ItemLink.URL

    print "Image: ", product.MediumImage.URL


    # http://docs.aws.amazon.com/AWSECommerceService/latest/DG/EX_RetrievingPriceInformation.html
    if hasattr(product, "OfferSummary"):

        if hasattr(product.OfferSummary, 'LowestNewPrice'):
            price = product.OfferSummary.LowestNewPrice.FormattedPrice
            print price

    print