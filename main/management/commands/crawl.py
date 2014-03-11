import json
import time
import urllib
import urllib2

import diffbot

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


from main.models import (
    CurrentUrl,
    Company,
    Media,
    ProductSingapore,
)    

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            country_code = args[0]
        except IndexError:
            self.stdout.write('Please supply country code')

        client = diffbot.Client(token=settings.DIFFBOT_TOKEN)

        count = 0
        if country_code == 'sg':
            urls = CurrentUrl.objects.filter(country=country_code)[:10]
            while (urls):
                for url in urls:
                    data = client.product(url.link)
                    product_json = data.get('products')

                    if product_json:
                        product_json = product_json[0]
                        product, created = ProductSingapore.objects.get_or_create(
                            product_id = product_json.get('productId'),
                            company = url.company
                        )

                        if created:
                            product.link = url.link
                            product.title = product_json.get('title')
                            product.description = product_json.get('description')
                            product.offer_price = float(product_json.get('offerPrice')) if product_json.get('offerPrice') else 0.0
                            product.regular_price = float(product_json.get('regularPrice')) if product_json.get('regularPrice') else 0.0
                            product.merchange = product_json.get('brand')

                            media_json = product_json.get('media')

                            if media_json:
                                media_json = media_json[0]
                                media_link = media_json.get('link')
                                media_caption = media_json.get('caption')
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
