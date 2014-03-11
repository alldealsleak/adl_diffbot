import os, sys
sys.path.append('/var/www/adl_diffbot/')
sys.path.append('/var/www/adl_diffbot/adl_diffbot/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'adl_diffbot.settings.dev'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
