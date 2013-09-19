# amazon api test

from amazonproduct import API, AWSError
access_key = "AKIAJ6HNZC6HWILISCKA"
secret_key = "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"
associate_tag = "6404-2547-9415"

api = API(access_key, secret_key, associate_tag=associate_tag, locale="us")

for page in api.item_search('MP3Downloads', Keywords='Daft Punk', ResponseGroup='Large'):
    for product in page.Items.Item:
        amazon_id = product.ASIN
        try:
            title = product.ItemAttributes.Title
        except:
            pass

        print amazon_id, title

        """
        Not sure how this is supposed to work there are
        hundreds of things in http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_response_elements.html
        and only some of them seem to be in the "product"
        """
        if hasattr(product.ItemAttributes, 'ListPrice'):
            print unicode(product.ItemAttributes.ListPrice.FormattedPrice)
        if hasattr(product.OfferSummary, 'LowestUsedPrice'):
            print u'(used from %s)' % product.OfferSummary.LowestUsedPrice.FormattedPrice
        if hasattr(product.ItemAttributes, 'Amount'):
            print unicode(product.ItemAttributes.Amount)

        # http://docs.aws.amazon.com/AWSECommerceService/latest/DG/EX_RetrievingPriceInformation.html
        if hasattr(product, "OfferSummary"):
            price = product.OfferSummary.LowestNewPrice.FormattedPrice
            print price
