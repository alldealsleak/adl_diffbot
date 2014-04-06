from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'adl_diffbot',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'autocommit': True,
        }
    },
    'dev': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'adl_diffbot_db',
        'USER': 'adl_postgres',
        'PASSWORD': 'Alldealsleak123',
        'HOST': '128.199.213.210',
        'PORT': '',
        'OPTIONS': {
            'autocommit': True,
        }
    }
}