# -*- coding: utf-8 -*-

import datetime
import json
import re

from django.http import HttpResponse

from .models import (
    ProductSingapore,
    ProductVietnam,
)

COUNTRY_CODES = [
    'sg',
    'vn',
]

PRODUCT_CLASSES = {
    'sg': ProductSingapore,
    'vn': ProductVietnam,
}

PRODUCT_TABLES = {
    'sg': 'main_productsingapore',
    'vn': 'main_productvietnam',
}

# We define country codes for new currencies
US_DOLLARS = 'us'
PE_SOLES = 'pe'
BR_REALES = 'br'
SG_DOLLARS = 'sg'
MY_DOLLARS = 'my'
PH_PESOS = 'ph'
ID_RUPIAH = 'id'
TH_BAHT = 'th'
HK_DOLLARS = 'hk'
VN_DONG = 'vn'


class JsonResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(self, content, mimetype='application/json', status=None,
                 content_type=None):
        super(JsonResponse, self).__init__(
            content=json.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )


def unix_to_datetime(unix_timestamp):
    return datetime.datetime.fromtimestamp(int(unix_timestamp))


def parse_float_price(text, country):
    if not text:
        return 0.0
    decimal_format_list = ['id','vn']
    text = text.replace(',', '')

    if country in decimal_format_list:
        text = text.replace('.', '')

    try:
        text = '%s' % re.findall('\d+', text)[0]
    except IndexError:
        return 0.0
    return float(text)
