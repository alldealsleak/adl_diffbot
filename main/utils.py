import datetime
import psycopg2

from django.conf import settings

from .models import ProductSingapore


PRODUCT_CLASSES = {
    'sg': ProductSingapore,
}


PRODUCT_TABLES = {
    'sg': 'main_productsingapore',
}

def unix_to_datetime(unix_timestamp):
    return datetime.datetime.fromtimestamp(int(unix_timestamp))
