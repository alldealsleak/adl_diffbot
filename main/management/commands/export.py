import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from openpyxl import Workbook

from main.models import (
    Company,
)
from main.utils import (
    PRODUCT_CLASSES,
)

class Command(BaseCommand):
    args = '<country_code>'
    help = 'Exports products into excel file'

    def handle(self, *args, **options):
        try:
            country_code = args[0]
            company_name = args[1]
        except IndexError:
            self.stdout.write('Please supply country code and company name')

        try:
            category_name = args[2]
        except:
            category_name = None

        product_class = PRODUCT_CLASSES[country_code]
        company = Company.objects.get(name__iexact=company_name)


        wb = Workbook(optimized_write = True)
        ws = wb.create_sheet()
        headers = [
            'COMPANY',
            'PRODUCT ID',
            'TITLE',
            'CATEGORY',
            'DESCRIPTION',
            'OFFER PRICE',
            'REGULAR PRICE',
            'BRAND',
            'URL',
            'MEDIA URL',
            'CREATED',
        ]

        ws.append(headers)

        date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_path = os.path.join(settings.MEDIA_ROOT, 'exports')

        idx = 0

        if not category_name:
            products = product_class.objects.filter(company=company)[idx:idx+10]
            file_name = os.path.join(
                file_path, 'Product-{0}-{1}.xlsx'.format(company_name, date_str)
            )
        else:
            products = product_class.objects.filter(company=company, category__name=category_name)[idx:idx+10]
            file_name = os.path.join(
                file_path, 'Product-{0}-{1}-{2}.xlsx'.format(company_name, category_name, date_str)
            )

        while products:
            for product in products:
                prod = [
                    product.company.name,
                    product.product_id,
                    product.title,
                    product.category.name if product.category else '',
                    product.description,
                    product.offer_price,
                    product.regular_price,
                    product.merchant,
                    product.link,
                    product.media.link if product.media else '',
                    product.created,
                ]
                ws.append(prod)
            idx += 10
            if not category_name:
                products = product_class.objects.filter(company=company)[idx:idx+10]
            else:
                products = product_class.objects.filter(company=company, category__name=category_name)[idx:idx+10]

        wb.save(file_name)

        print 'File {} saved'.format(file_name)