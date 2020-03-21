# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u0979652/data/www/nebezdari.ru/nebezdariproject')
sys.path.insert(1, '/var/www/u0979652/data/djangovenv/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nebezdariproject.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()