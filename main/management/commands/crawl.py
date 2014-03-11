import json
import time
import urllib
import urllib2

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from main.models import (
    CurrentUrl,
    Company,
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

        count = 0
        if country_code == 'sg':
            urls = CurrentUrl.objects.filter(country=country_code)[:10]
            while (urls):
                for url in urls:
                    url_crawl = '{}?token={}&url={}'.format(settings.DIFFBOT_URL, settings.DIFFBOT_TOKEN, url.link)
                    response = urllib2.urlopen(url_crawl)
                    data = json.load(response)
                    product_json = data['products'][0]
                    product, created = ProductSingapore.objects.get_or_create(product_id=product_json['productId'], company=url.company)

                    if created:
                        product.link = url
                        product.title = product_json['title']
                        product.description = product_json['description']
                        product.offer_price = product_json['offerPrice']
                        product.merchange = product_json['brand']
                        product.save()

                    url.delete()
                    urls = CurrentUrl.objects.filter(country=country_code)[:10]
                    count += 1
                    time.sleep(1)
        self.stdout.write('Successfully crawled %s urls' % count)
