# -*- coding: utf-8 -*-

import time

import diffbot

from django.conf import settings
from django.core.management.base import BaseCommand

from main.models import (
    CurrentUrl,
    Media,
)
from main.utils import (
    COUNTRY_CODES,
    PRODUCT_CLASSES,
    parse_float_price,
)


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            country_code = args[0]
            company_name = args[1]
        except IndexError:
            self.stdout.write('Please supply country code')

        client = diffbot.Client(token=settings.DIFFBOT_TOKEN)

        count = 0
        if country_code in COUNTRY_CODES:
            product_class = PRODUCT_CLASSES[country_code]
            urls = CurrentUrl.objects.filter(
                country=country_code, company__name=company_name).order_by('-added')[:10]
            while (urls):
                for url in urls:
                    print url.link
                    data = client.product(url.link)
                    product_json = data.get('products')

                    if product_json:
                        product_json = product_json[0]
                        product, created = product_class.objects.get_or_create(
                            product_id = product_json.get('productId'),
                            company = url.company
                        )
                        if created:
                            offer_price = product_json.get('offerPrice') if product_json.get('offerPrice') else '0'
                            offer_price = parse_float_price(offer_price, country_code)

                            regular_price = product_json.get('regularPrice') if product_json.get('regularPrice') else '0'
                            regular_price = parse_float_price(regular_price, country_code)

                            save_amt = product_json.get('saveAmount') if product_json.get('saveAmount') else '0'
                            save_amt = parse_float_price(save_amt, country_code)

                            title = product_json.get('title')
                            description = product_json.get('description') if product_json.get('description') else ''
                            merchant = url.merchant if url.merchant else product_json.get('brand')

                            if not offer_price and (regular_price and save_amt):
                                offer_price = regular_price - save_amt

                            product.link = url.link
                            product.category = url.category
                            product.merchant = url.merchant
                            product.title = u'{}'.format(title).encode('utf-8')
                            product.description = u'{}'.format(description).encode('utf-8')
                            product.offer_price = offer_price
                            product.regular_price = regular_price
                            product.merchant = merchant

                            media_json = product_json.get('media')

                            if media_json:
                                media_json = media_json[0]
                                media_link = media_json.get('link')
                                media_caption = media_json.get('caption') if media_json.get('caption') else 'No caption'
                                media, created = Media.objects.get_or_create(
                                    caption = media_caption,
                                    link = media_link
                                )
                                product.media = media
                        product.save()

                    url.delete()
                    urls = CurrentUrl.objects.filter(country=country_code)[:10]
                    count += 1
                    time.sleep(1)
            self.stdout.write('Successfully crawled %s urls' % count)
        else:
            self.stdout.write('Invalid country code')
