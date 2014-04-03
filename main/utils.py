# -*- coding: utf-8 -*-

import datetime
import psycopg2
import re
import regex

from django.conf import settings

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



def unix_to_datetime(unix_timestamp):
    return datetime.datetime.fromtimestamp(int(unix_timestamp))


def parse_float_price(text, country):
    if not text:
        return 0.0
    decimal_format_list = ['id','vn']
    text = text.replace(',', '')

    if country in decimal_format_list:
        text = text.replace('.', '')

    text = '%s' % re.findall('\d+', text)[0]
    return float(text)        
