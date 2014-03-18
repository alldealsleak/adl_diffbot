import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from openpyxl import Workbook

from main.models import (
    ProductSingapore,
)

class Command(BaseCommand):
    args = '<country_code>'
    help = 'Exports products into excel file'

    def handle(self, *args, **options):
        try:
            country_code = args[0]
        except IndexError:
            self.stdout.write('Please supply country code')

        wb = Workbook(optimized_write = True)
        ws = wb.create_sheet()
        headers = [
            'COMPANY',
            'ID',
            'TITLE',
            'DESCRIPTION',
            'OFFER PRICE',
            'REGULAR PRICE',
            'BRAND',
            'URL',
            'MEDIA URL',
            'CREATED',
        ]

        ws.append(headers)

        products = ProductSingapore.objects.all()

        for product in products:
            prod = [
                product.company.name,
                product.product_id,
                product.title,
                product.description,
                product.offer_price,
                product.regular_price,
                product.merchant,
                product.link,
                product.media.link if product.media else '',
                product.created,
            ]
            ws.append(prod)

        date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_path = os.path.join(settings.MEDIA_ROOT, 'exports')
        file_name = os.path.join(
            file_path, 'Product-{}.xlsx'.format(date_str)
        )
        wb.save(file_name)

        print 'File {} saved'.format(file_name)